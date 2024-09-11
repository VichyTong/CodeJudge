import json


def pre_process_conala_data():
    with open("./data/conala/conala_grade.json", "r") as f:
        data = json.load(f)

    out = []
    for i in data:
        item = {
            "intent": i["intent"],
            "snippet": i["snippet"][0],
            "baseline": i["baseline"],
            "tranx-annot": i["tranx-annot"],
            "best-tranx": i["best-tranx"],
            "best-tranx-rerank": i["best-tranx-rerank"],
            "codex": i["codex"],
            "grade": {
                "baseline": i["grade-baseline"],
                "tranx-annot": i["grade-tranx-annot"],
                "best-tranx": i["grade-best-tranx"],
                "best-tranx-rerank": i["grade-best-tranx-rerank"],
                "codex": i["grade-codex"],
            },
        }
        out.append(item)

    with open("./data/conala/conala.json", "w") as f:
        json.dump(out, f, indent=4)


if __name__ == "__main__":
    pre_process_conala_data()
