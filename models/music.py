from typing import Optional, List

from pydantic import BaseModel

class MusicInfo(BaseModel):
    id: str
    name: str
    artist: str
    genres: Optional[List[str]]
    description: Optional[str]
    music_rep_audio: Optional[str] # Path to a folder that contains music representation of a piece.  
    music_rep_symbolic: str 

    class Config:
        schema_extra = {
            'id': 'iqwurui132409r90wef9asdf', 
            'name': 'Ode to Joy', 
            'artist': 'Ludwig van Beethoven', 
            'description': ' ... some description about the song and its context ... ', 
            'music_rep_audio': '../../..where you would like to place its audio representation', 
            'music_rep_symbolic': '', 
        }
