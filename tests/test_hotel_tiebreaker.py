from helpers import run_cli


def test_hotel_tiebreaker(tmp_path):
    reservas = [
        {"hotel_id": "H03", "amount": "500.00"},
        {"hotel_id": "H01", "amount": "500.00"},
        {"hotel_id": "H02", "amount": "500.00"},
    ]

    report = run_cli(tmp_path, reservas, top=2)

    ids = [hotel["hotel_id"] for hotel in report["top_hotels"]]

    assert ids == ["H01", "H02"]