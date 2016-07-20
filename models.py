#home 1 or 0
#opponent
#runs
#opp_runs
#gameid
#date

#$  sudo -u postgres createdb penaax

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlutils import get_or_create
import calendar

engine = create_engine('postgresql://postgres:joseph@localhost/penaax')

Base = declarative_base()
Session = sessionmaker(bind=engine)

class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, Sequence("game_id_seq"), primary_key=True)
    home = Column(Integer)
    oppo = Column(String)
    pens_runs = Column(String)
    oppo_runs = Column(String)
    gameid = Column(String)
    lookupdate = Column(String)

    def parse_info(self, info, lookupdate):
        self.lookupdate = lookupdate
        for i in info:
            if "Pensacola" in i['team']:
                self.pens_runs = i['runs']
                if "home" in i['location']:
                    self.home = 1
                if "away" in i['location']:
                    self.home = 0
            else:
                self.oppo_runs = i['runs']
                self.oppo = str(i['team'])

class LookupDate(Base):
    __tablename__ = "date"
    id = Column(Integer, Sequence("game_id_seq"), primary_key=True)
    yyyymmdd = Column(String)
    finished = Column(Integer)

Base.metadata.create_all(engine)

s = Session()

_MONTHS = [4, 5, 6, 7, 8, 9]
_YEARS = [2012, 2013, 2014, 2015, 2016]

def build_dates():
    dates = []
    for year in _YEARS:
        for month in _MONTHS:
            for day in range(1, calendar.monthrange(year, month)[1]+1):
                dates.append("{}{}{}".format(year, str(month).zfill(2), str(day).zfill(2)))
    return dates


def main():
    dates = build_dates()
    for date in dates:
        d, c = get_or_create(s, LookupDate, yyyymmdd=date)
    s.commit()

if __name__ == "__main__":
	main()
	print len(s.query(LookupDate).all())
