import json

with open("category.json", "w") as f:
    cate = {}
    for i, c in enumerate([["food", 100000], ["rent", 1000000], ["entertaining", 50000]]):
        cate[i] = {}
        cate[i]["name"] = c[0]
        cate[i]["range"] = c[1]
    json.dump(cate, f, indent=4)

