# Spenser's Color Wheel

An experimental poetry project by [John R. Ladd](https://jrladd.com).

Part data visualization and part poetry generator, *Spenser's Color Wheel* is an exploration of the color words the poet uses in his two most famous works, *The Faerie Queene* and *The Shepheardes Calender*.  What color words does Spenser choose and in what proportions? What color terms appear in his epic versus his pastoral? How does he deploy color within the economy of his lines and stanzas?

Following from Jerome McGann's notion of "deformance," the project takes Spenser's poetry apart and reassembles it to illuminate Spenser's use of color for different poetic purposes. By scrolling among the pie charts, the viewer can quickly see which colors Spenser includes from book to book in *The Faerie Queene* and month to month in *The Shepheardes Calender*. The circles are scaled according to the proportion of lines that have color terms to the whole of each text, which gives the viewer a quick sense of how much Spenser uses color in each poem section.

By clicking on the colors, the viewer can make poems out of randomly selected "color-lines" from that text. The new poems---fourteen lines long, as Spenser was a writer of sonnets among many other things---will always contain lines proportional to the usage of color the viewer clicked. But since the lines are chosen at random and can be reordered at will, it's unlikely to ever encounter the same fourteen-line poem twice. The resulting poems, like those in [The Mutable Stanzas](https://robineggsky.com/apps/mutableStanzas/), show that Spenser's lines are self-contained enough to be reordered into new senses. But by including only lines with color words, the new poems have greater density of striking images.

What can we see with this project that is harder to see by reading? Since making it, I've noticed that Book IV of *The Faerie Queene* has more silver, Spenser's color for water, while Book VI has more green, commensurate with the return of Colin Clout and Spenser's reuse of pastoral themes. Purple, Spenser's color for blood and gore, shows up more in the second, social half of *The Faerie Queene* than the first. Combining lines from these different moments into new poems produces dizzying effects.

[A note on "red": Initially the graphs showed much more red, but only because many instances of "read" were not being properly modernized. Poems with lots of reading, like Book I, showed lots of the color red by mistake (a happy mistake, perhaps!). I wrote manual rules to handle most of the mistaken "red" terms, but a few may have made it through.]

The project was generated with the regularized-spelling texts available from [EarlyPrint](https://earlyprint.org) and the color words found in the [WordNet](http://wordnet.princeton.edu/) hierarchy. The search for relevant lines was done in Python, while the visualization and poetry generation was done in JavaScript, especially [D3.js](https://d3js.org). The project went through several iterations before this current version, and all the code is available in the [Github repository](https://github.com/jrladd/colorwheel).

The project is housed [here](https://jrladd.com/colorwheel).
