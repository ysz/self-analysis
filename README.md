# analyze where Toggl time goes

Export "Detailed" Report from Toggl for a "Client" and run 

```
./toggl.py Toggl_time_entries_blahblah
```

to get `out.png` with heatmap where 

- red means full hour was tracked 

- less red means it was something like 15:30 to 16:20 which spans 2 wall clock hours 

![](/out.png)

