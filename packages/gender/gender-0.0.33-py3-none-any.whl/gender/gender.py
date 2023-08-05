import json
from string import ascii_lowercase
import os
import re  # type: ignore
from typing import NamedTuple, Optional, Dict
from types import MappingProxyType
from collections import Counter, defaultdict


class Person(NamedTuple):
    """
    this class represents a person
    """

    title: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    gender: Optional[str]


class GenderDetector:
    """
    detects gender from a string
    """

    GENDERS = ["m", "f"]
    AFFIXES = "al bar el de da du das los la le van dos del della di der ter e".split()

    def __init__(self) -> None:

        self.saluts = json.load(
            open(os.path.join(os.path.dirname(__file__), "data/data_salutations_.json"))
        )
        self.first_names = MappingProxyType(
            json.load(
                open(os.path.join(os.path.dirname(__file__), "data/data_names_.json"))
            )
        )

        self.last_names = {
            stripped_line
            for line in open(
                os.path.join(os.path.dirname(__file__), "data/data_last_names_.txt")
            )
            if (stripped_line := line.strip())
        }
        self.hypocs = json.load(
            open(os.path.join(os.path.dirname(__file__), "data/data_hypocorisms_.json"))
        )

        self.gramms = MappingProxyType(
            json.load(
                open(
                    os.path.join(
                        os.path.dirname(__file__), "data/data_grammgender_.json"
                    )
                )
            )
        )

        # when the ASCII flag is used, \w is [a-zA-Z0-9_]
        self.email_pattern = re.compile(
            r"^[a-z]+[\w\.\-]+[a-z0-9]+\@{1}[a-z0-9]+[\w\.]+[a-z]$", flags=re.ASCII
        )

    def _from_title(self, title: Optional[str]) -> Optional[str]:
        """
        find and return gerder according to the title string; if failed to find, return None
        """
        for g in self.GENDERS:
            if {title} & set(self.saluts["common"][g] + self.saluts["uncommon"][g]):
                return g

    def _from_first_name(self, first_name: Optional[str]) -> Optional[str]:
        """
        find and return gerder according to the first_name string; if failed to find, return None
        """
        if found_first_name := self.first_names.get(first_name, None):
            return found_first_name

        if first_name in self.hypocs:
            possible_genders = {
                self.first_names[nm]
                for nm in (set(self.hypocs[first_name]) & set(self.first_names))
            }
            if len(possible_genders) > 0:
                return possible_genders.pop()

    def _fromlist_of_words_in_email(self, email: Optional[str] = None) -> Optional[str]:
        """
        find and return gerder according to the email string; if failed to find, return None
        """
        if email is None:
            return None

        list_of_words_in_email = re.split(r"[\s\-\.\_]", email.split("@")[0])

        # keep potential genders based in first names in here
        first_name_gender_candidates = set()

        # similar temporary storage for genders derived from the
        # grammatical gender words found in email address
        gramm_gender_candidates = set()

        for word in list_of_words_in_email:
            _g = self._from_first_name(word)
            if _g:
                first_name_gender_candidates.add(_g)
            for w in self.gramms:
                if (w in word) and (self.gramms[w] in self.GENDERS):
                    gramm_gender_candidates.add(self.gramms[w])

        # if one of these candidate sets has a single
        # candidate then we pick it as gender
        for s in (list(first_name_gender_candidates) + list(gramm_gender_candidates)):
            if s in self.GENDERS:
                return s

    def get_gender(self, st: str) -> "Person":

        # pre-process string first
        st_ = str(st).lower().strip()

        for _ in st_.split():
            if foundlist_of_words_in_email := re.search(self.email_pattern, _):
                email = foundlist_of_words_in_email.group(0)
                st_ = "".join(st_.split(email)[:-1])
            else:
                email = None

        st_ = re.sub(
            r"\s+", " ", re.sub(r"[^" + ascii_lowercase + r"]", " ", st_)
        ).strip()

        # try to find any titles
        title_candidates = set()

        for type_ in "common uncommon".split():
            for g in self.saluts[type_]:
                tt_ = set(self.saluts[type_][g]) & set(st_.split())
                if tt_:
                    title_candidates |= tt_

        # now to the first name; assume that first name is more likely to stand before the last name
        first_name_candidates = []

        for _ in st_.split():
            if _ in self.first_names:
                if self.first_names[_] in self.GENDERS:
                    first_name = _
                    break
                else:
                    # it's a unisex name, add to candidates
                    first_name_candidates.append(_)

        # some names can be like title_candidates, e.g. Dean
        names_like_titles = set(first_name_candidates) & title_candidates

        if names_like_titles:
            # priority to names
            title = (title_candidates - names_like_titles).pop()
            first_name = names_like_titles.pop()
            st_ = " ".join([_ for _ in st_.split() if _ != title])
        elif title_candidates:
            title = title_candidates.pop()
        else:
            title = None

        if (not first_name) and first_name_candidates:
            first_name = first_name_candidates[0]
        elif not first_name:
            for _ in st_.split():
                if _ in self.hypocs:
                    first_name = _
                    break

        if first_name:
            st_ = " ".join([_ for _ in st_.split() if _ != first_name]).strip()

        # what's the last name then? assume it's more likely to come last
        if st_:
            wrds = st_.split()
            known_lnames = self.last_names & set(wrds)
            if len(known_lnames) == 1:
                last_name = known_lnames.pop()
            elif len(wrds) == 1:
                last_name = wrds[-1]
            elif wrds[-2] not in self.AFFIXES:
                last_name = wrds[-1]
            else:
                last_name = " ".join(wrds[-2:])

        gender_from = defaultdict()

        gender_from["title"] = self._from_title(title)
        gender_from["first_name"] = self._from_first_name(first_name)
        gender_from["email"] = self._fromlist_of_words_in_email(email)

        # if gender derived from just one source is available
        if sum((v is not None) for v in gender_from.values()) == 1:
            for what in gender_from:
                if gender_from[what]:
                    selected_gender = gender_from[what]

        if all(
            [
                gender_from["title"],
                gender_from["first_name"],
                gender_from["title"] == gender_from["first_name"],
            ]
        ):
            selected_gender = gender_from["first_name"]

        if all(
            [
                gender_from["title"],
                gender_from["first_name"],
                gender_from["title"] != gender_from["first_name"],
                gender_from["email"],
            ]
        ):
            if (gender_from["email"] == gender_from["title"]) or (
                gender_from["email"] == gender_from["first_name"]
            ):
                selected_gender = gender_from["email"]

        if all(
            [gender_from["title"], gender_from["first_name"], not gender_from["email"]]
        ):
            selected_gender = gender_from["title"]

        if all([not gender_from["title"], gender_from["first_name"]]):
            selected_gender = gender_from["first_name"]

        if all(
            [
                not gender_from["title"],
                not gender_from["first_name"],
                gender_from["email"],
            ]
        ):
            selected_gender = gender_from["email"]

        return Person(
            title=title,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=selected_gender,
        )

    def update_first_names(self, new_first_names: Dict[str, str]) -> None:

        first_names = json.load(
            open(os.path.join(os.path.dirname(__file__), "data/data_names_.json"))
        )

        __update_dict = defaultdict()

        for new_first_name in new_first_names:

            if new_first_name in first_names:

                if first_names[new_first_name] == new_first_names[new_first_name]:
                    print(f"name {new_first_name} is already in the database")
                elif first_names[new_first_name] != "u":
                    __update_dict[new_first_name] = "u"
                    print(
                        f"updating gender for name {new_first_name}: now it's {__update_dict[new_first_name]} (was {first_names[new_first_name]})"
                    )
            else:
                __update_dict[new_first_name] = new_first_names[new_first_name]
                print(
                    f"adding new name {new_first_name} ({new_first_names[new_first_name]})"
                )

        first_names.update(__update_dict)

        gender_counts = Counter(first_names.values())
        print(
            f'male names: {gender_counts["m"]:,} female names: {gender_counts["f"]:,} unisex names: {gender_counts["u"]:,}'
        )
        print(f"total names: {sum(gender_counts.values()):,}")

        json.dump(
            first_names,
            open(os.path.join(os.path.dirname(__file__), "data/data_names_.json"), "w"),
        )
