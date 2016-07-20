import csv, os
from models import Session, Game

session = Session()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    fields = get_field_names()
    with open(os.path.join(ROOT_DIR, 'penaax.csv'), 'w') as f:
        write_scoreboard(fields, f)

def write_scoreboard(modelinfo, f):
    writer = csv.writer(f, csv.excel)
    header = modelinfo
    writer.writerow(header)
    for game in session.query(Game).all():
        row = [getattr(game, x) for x in modelInfo]
        writer.writerow(row)

def get_field_names():
    fields = []
    for c in Game.__table__.columns:
        fields.append(c.name)

    return fields

if __name__ == "__main__":
    main()
