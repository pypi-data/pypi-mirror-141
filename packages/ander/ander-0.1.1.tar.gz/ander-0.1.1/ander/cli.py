from typing import Set

import fire


def ander(filename1: str, filename2: str) -> Set[str]:
    with open(filename1) as f1, open(filename2) as f2:
        set1: Set[str] = set([s.strip() for s in f1.readlines() if s.strip() != ""])
        set2: Set[str] = set([s.strip() for s in f2.readlines() if s.strip() != ""])
    res_set: Set[str] = set1.intersection(set2)
    return res_set


def main() -> int:
    fire.Fire(ander)
    return 0


if __name__ == "__main__":
    main()
