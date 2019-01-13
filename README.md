# smh
smh, short for Shake My Head, is a desktop game created in PyGame and OpenCV with the objective to avoid hitting enemies by moving your head from side to side while bobbing to the song in the background. The enemies are procedurally generated so that the enemies appear according to the music and your head moves according to the beat.

This game was designed for [Hack112 F17](https://www.cs.cmu.edu/~112/), one Carnegie Mellon University's largest hackathons, along with team members [Komal Dewan](mailto:kdewan@andrew.cmu.edu), [Kusha Maharshi](mailto:kmaharsh@andrew.cmu.edu), and [Sebastien La Duca](mailto:sladuca@andrew.cmu.edu).

### Dependancies
* `pygame`
* `cv2`
* `face_recognition`
* `matplotlib`
* `numpy`
* `scipy`
* `sobol`

### Installation
1. Add a webcam picture of the player(s) into `./players/`.
2. To add a new song, add its `.wav` file to `./music/` and run `processor.py` replacing the song name on line 21.
3. To play with the new song, run `game.py` replacing the song name on line 21.

**NOTE:** The process versions of songs Shape of You by Ed Sheeran and Spectre by Alan Walker are included in `./json/` but not the actual `.wav` file.
