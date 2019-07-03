`-A` add to the end.
-i insert at the current position
-a the same as -i
:q! exit the editing without save
-d delete menu
    -dw delete till the end of the current word
    -d$ delete till the end of the line
    -de delete from the current cursor to the end of the word
-[num][we] move to the next `num` word
-0 move to the start of the line
-d[num]w delete the next num of words
-[num]dd delete the following num of lines. Actually it cuts the line. usd -p to paste the line.
-u redo the commands
    like ctrl+z
    -U redo the changes to the entire line.
    ctrl + r can return the previous changes, including the undos.
-p put the deleted text after the cursor.
-r replace the char with the next char inputed.
-ce delete from the current cursor till the end of the current word, and change mode into Insert. serves like change the word.
    -c$ equals to d$+i delete till the end and change to Insert mode.
    -c[num]w Change the following num of words.
-G go to the button of the file.
    -gg go to the head of the file.
    -[num]G go to the num line.



