import csv
from io import StringIO

from mast_parser.models import FamousPerson


class LastFamousPersonToCSVGenerator:
    FIELDNAMES = [
        "id",
        "english_url",
        "english_name",
        "english_text",
        "russian_url",
        "russian_name",
        "russian_text",
    ]

    @classmethod
    def person_to_dict(cls, person: FamousPerson):
        return {field: getattr(person, field) for field in cls.FIELDNAMES}

    def execute(self, famous_persons: list[FamousPerson]) -> StringIO:
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=self.FIELDNAMES, delimiter=";")
        writer.writeheader()
        writer.writerows(self.person_to_dict(person) for person in famous_persons)

        output.seek(0)

        return output
