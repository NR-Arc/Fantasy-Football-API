"""FastAPI project main file."""
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from datetime import date

import chapter4.schemas as schemas
import chapter4.crud as crud
from chapter4.database import SessionLocal

#app = FastAPI(title="Fantasy Football API", version="1.0.0")
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Fantasy Football API!"}

@app.get("/V0/players/", response_model=list[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, 
                 minimum_last_changed_date: date | None = None,
                 first_name: str | None = None,
                 last_name: str | None = None,
                 db: Session = Depends(get_db)
                 ):
    players = crud.get_players(db, 
                               skip=skip, limit=limit,
                               min_last_changed_date=minimum_last_changed_date
                               first_name=first_name,
                               last_name=last_name)
    return players

@app.get("/V0/players/{player_id", response_model=list[schemas.Player])
def read_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.get("/v0/performances/", response_model=list[schemas.Performance])
def read_performances(skip: int = 0, limit: int = 100,
                      minimum_last_changed_date: date | None = None,
                      db: Session = Depends(get_db)):
    performances = crud.get_performances(db, 
                                         skip=skip, limit=limit,
                                         min_last_changed_date=minimum_last_changed_date)
    return performances

@app.get("/v0/leagues/{league_id}", response_model=schemas.League)
def read_league(league_id: int, db: Session = Depends(get_db)):
    league = crud.get_league(db, league_id=league_id)
    if league is None:
        raise HTTPException(status_code=404, detail="League not found")
    return league

@app.get("/v0/leagues/", response_model=list[schemas.League])
def read_leagues(skip: int = 0, limit: int = 100,
                 minimum_last_changed_date: date | None = None,
                 league_name: str | None = None,
                 db: Session = Depends(get_db)):
    leagues = crud.get_leagues(db, skip=skip, limit=limit,
                               min_last_changed_date=minimum_last_changed_date,
                               league_name=league_name)
    return leagues

@app.get("/v0/teams/", response_model=schemas.Team)
def read_team(skip: int = 0, limit: int = 100,
              minimum_last_changed_date: date | None = None,
              team_name: str | None = None,
              league_id: int | None = None,
              db: Session = Depends(get_db)):
    teams = crud.get_team(db, skip=skip, limit=limit,
                         min_last_changed_date=minimum_last_changed_date,
                         team_name=team_name,
                         league_id=league_id)
    return teams

@app.get("/v0/counts/", response_model=schemas.Counts)
def get_counts(db: Session = Depends(get_db)):
    counts = schemas.Counts(
        league_count = crud.get_league_count(db),
        team_count = crud.get_team_count(db),
        player_count = crud.get_player_count(db)
    )
    return counts