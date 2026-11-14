from helpers import run_cli


def test_process_all_reservations(tmp_path):
    reservas = []

    for numero in range(201):
        reservas.append({
            "reservation_id": f"R-{numero}"
        })

    report = run_cli(tmp_path, reservas)

    assert report["summary"]["total_reservations"] == 201