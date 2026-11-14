from helpers import run_cli


def test_round_only_after_sum(tmp_path):
    reservas = [
        {"reservation_id": "R-1", "amount": "0.005"},
        {"reservation_id": "R-2", "amount": "0.005"},
    ]

    report = run_cli(tmp_path, reservas)

    assert report["summary"]["total_amount_brl"] == "0.01"



def test_round_half_up(tmp_path):
    reservas = [
        {"reservation_id": "R-1", "amount": "0.005"}
    ]

    report = run_cli(tmp_path, reservas)

    assert report["summary"]["total_amount_brl"] == "0.01"