from task2.solution import count_by_first_letter, fetch_category_members
from unittest.mock import patch


def test_count_by_first_letter_simple():
    titles = ["Антилопа", "Аист", "Бобр", "Белка", "Волк"]
    expected = {"А": 2, "Б": 2, "В": 1}
    result = count_by_first_letter(titles)
    assert result == expected


@patch("task2.solution.requests.get")
def test_fetch_category_members_mocked(mock_get):
    mock_get.return_value.json.return_value = {
        "query": {
            "categorymembers": [
                {"title": "Акула"},
                {"title": "Барсук"},
            ]
        }
    }

    members = fetch_category_members("Категория:Животные_по_алфавиту")
    assert isinstance(members, list)
    assert members[0]["title"] == "Акула"
    assert members[1]["title"] == "Барсук"
