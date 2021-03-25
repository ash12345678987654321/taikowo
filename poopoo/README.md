# taikowo

Stuff you need:

```
pip install librosa
conda install -c conda-forge ffmpeg
```



How taiko maps are stored (attempt at reading it):

there are stored by `x,y,time,obj,sound,???:???`

obj=1 if it is a normal note

sound has bit 8 if its blue

sound has bit 4 if its finisher

