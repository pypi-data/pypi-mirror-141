import argparse
import difflib
import os
from dataclasses import dataclass, field
from typing import Generator, Optional, Sequence

from git import Commit, Diff, Head, Repo

# Possible change types for diff objects (from https://git-scm.com/docs/git-diff#_raw_output_format):
CHANGE_TYPES = {
    "A": "addition of a file",
    "C": "copy of a file into a new one",
    "D": "deletion of a file",
    "M": "modification of the contents or mode of a file",
    "R": "renaming of a file",
    "T": "change in the type of the file (regular file, symbolic link or submodule)",
    "U": "file is unmerged (you must complete the merge before it can be committed)",
    "X": '"unknown" change type (most probably a bug, please report it)',
}

SUPPORTED_CHANGE_TYPES = {"A", "M"}

DEFAULT_DESIRED_MAX_LINE_CHANGES = 500


@dataclass(frozen=True)
class ChangedFile:
    path: str
    lines: list[str] = field(repr=False)
    n_lines_added: int
    n_lines_deleted: int

    @property
    def n_lines_changed(self) -> int:
        return self.n_lines_added + self.n_lines_deleted


@dataclass(frozen=True)
class LineChangeStats:
    total: int
    added: int
    deleted: int


def get_changed_files(base_commit: Commit, target_commit: Commit) -> list[ChangedFile]:
    diff_list: list[Diff] = base_commit.diff(target_commit)

    for diff in diff_list:
        if diff.change_type not in SUPPORTED_CHANGE_TYPES:
            file_path = diff.b_path or diff.a_path
            raise RuntimeError(
                f"Unsupported change type for file {file_path!r}: "
                f"{diff.change_type!r} - {CHANGE_TYPES[diff.change_type]}. "
                f"Supported changes types: {sorted(SUPPORTED_CHANGE_TYPES)}"
            )

    changed_files: list[ChangedFile] = []
    for diff in diff_list:
        file_path = diff.b_path or diff.a_path
        n_lines_added = 0
        n_lines_deleted = 0

        if diff.change_type == "A":
            new_file_lines = diff.b_blob.data_stream.read().decode("utf-8").splitlines(keepends=True)
            n_lines_added = len(new_file_lines)
        else:
            old_file_lines = diff.a_blob.data_stream.read().decode("utf-8").splitlines(keepends=True)
            new_file_lines = diff.b_blob.data_stream.read().decode("utf-8").splitlines(keepends=True)
            differ_diff_generator = difflib.Differ().compare(old_file_lines, new_file_lines)
            for diff_line in differ_diff_generator:
                if diff_line.startswith("+ "):
                    n_lines_added += 1
                elif diff_line.startswith("- "):
                    n_lines_deleted += 1

        changed_files.append(
            ChangedFile(
                file_path,
                new_file_lines,
                n_lines_added,
                n_lines_deleted,
            ),
        )

    return changed_files


def compute_change_stats(changed_files: list[ChangedFile]) -> LineChangeStats:
    added, deleted = 0, 0
    for cf in changed_files:
        added += cf.n_lines_added
        deleted += cf.n_lines_deleted

    return LineChangeStats(added + deleted, added, deleted)


def split_changed_files(
    changed_files: list[ChangedFile],
    desired_max_line_changes: int,
) -> Generator[list[ChangedFile], None, None]:
    block: list[ChangedFile] = []
    block_line_changes = 0

    for cf in changed_files:
        tentative_line_changes = block_line_changes + cf.n_lines_changed
        if tentative_line_changes <= desired_max_line_changes:
            # Changed file fits in current block
            block.append(cf)
            block_line_changes = tentative_line_changes
        else:
            # Changed file doesn't fit in current block
            if block:
                yield block
                block = [cf]
                block_line_changes = cf.n_lines_changed
            else:
                yield [cf]
                block = []
                block_line_changes = 0

    if block:
        yield block


def create_split_branches(
    repo: Repo,
    source_branch: Head,
    target_commit: Commit,
    base_commit: Commit,
    split_blocks: list[list[ChangedFile]],
) -> None:
    original_commit_title = target_commit.message.splitlines()[0]

    for i, block in enumerate(split_blocks):
        block_n = i + 1
        new_branch_name = f"{source_branch}-part{block_n}"

        print(f"Creating split branch {new_branch_name!r}...")
        if new_branch_name in repo.branches:
            print("  Deleting pre-existing branch with the same name")
            repo.delete_head(new_branch_name, force=True)

        print("  Creating new branch")
        new_branch = repo.create_head(new_branch_name, commit=base_commit)

        print("  Checking out new branch")
        new_branch.checkout()

        print("  Writing file changes")
        written_file_paths = []
        for cf in block:
            full_file_path = os.path.join(repo.working_dir, cf.path)

            with open(full_file_path, "w") as fh:
                fh.writelines(cf.lines)

            written_file_paths.append(cf.path)

        print("  Adding files to Git index")
        repo.index.add(written_file_paths)

        print("  Committing changes")
        repo.index.commit(f"{original_commit_title} (part {block_n}/{len(split_blocks)})", skip_hooks=True)

        print("  Done")

    print(f"Checking out original branch {str(source_branch)!r}")
    source_branch.checkout()


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_dir", help="Path to the Git repository to work with")
    parser.add_argument(
        "-l",
        "--desired-max-line-changes",
        type=int,
        default=DEFAULT_DESIRED_MAX_LINE_CHANGES,
        help=f"Desired maximum line changes per split block (default: {DEFAULT_DESIRED_MAX_LINE_CHANGES}).",
    )
    args = parser.parse_args()

    repo_dir = os.path.abspath(args.repo_dir)
    desired_max_line_changes: int = args.desired_max_line_changes

    repo = Repo(repo_dir)
    print(f"Repository: {repo_dir}")

    source_branch: Head = repo.active_branch
    print(f"Branch: {source_branch}")

    target_commit: Commit = source_branch.commit
    print(f"Target commit: {target_commit}")

    if len(target_commit.parents) > 1:
        raise RuntimeError(
            f"Head SHA {target_commit} for branch {str(source_branch)!r} mustn't have more than one parent commit."
        )
    elif len(target_commit.parents) == 0:
        raise RuntimeError(
            f"Head SHA {target_commit} for branch {str(source_branch)!r} cannot be the initial repository commit."
        )

    if repo.untracked_files:
        raise RuntimeError(f"Repository {repo_dir!r} mustn't have untracked files")
    if repo.is_dirty():
        raise RuntimeError(f"Repository {repo_dir!r} mustn't have staged files")

    base_commit: Commit = target_commit.parents[0]
    print(f"Base commit: {base_commit}")

    print("Computing changes...")
    changed_files = get_changed_files(base_commit, target_commit)

    change_stats = compute_change_stats(changed_files)
    print(
        f"  Detected {len(changed_files)} files changed with {change_stats.total} lines changed "
        f"(+{change_stats.added}, -{change_stats.deleted})"
    )

    if change_stats.total <= desired_max_line_changes:
        print(
            f"Line changes do not exceed desired maximum line changes ({desired_max_line_changes}) "
            "-- nothing to do here"
        )
        return 0

    print(f"Splitting changes into parts with desired_max_line_changes={desired_max_line_changes}")
    split_blocks = list(split_changed_files(changed_files, desired_max_line_changes))

    print("Split breakdown:")
    for i, block in enumerate(split_blocks):
        block_n = i + 1
        stats = compute_change_stats(block)
        print(
            f"- Part {block_n}/{len(split_blocks)}. {len(block)} files changed with {stats.total} lines changed "
            f"(+{stats.added}, -{stats.deleted})"
        )

    res = input("Create split branches (y/N)?: ").lower()
    if res in ("y", "yes"):
        create_split_branches(repo, source_branch, target_commit, base_commit, split_blocks)
    else:
        print("Skipping creation of split branches")

    print("All done!")

    return 0


if __name__ == "__main__":
    exit(main())
