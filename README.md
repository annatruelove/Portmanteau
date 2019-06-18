# Portmanteau


This program creates a lexical blend of words. It takes in two words, parses them, and determines the best way to blend them. 

A blend is a word formed from two or more other words. A portmanteau is a specific type of blend, defined as a new word that is formed by joining two others and combining their meanings. This program works to create these types of blends. 

I used three different types of formations to determine the blends and used syllables as a basis for clipping the words. 

Formation 1 is where the end of one word is appended to the beginning of the other. This involves clipping because the two words are shortened and then combined. Some examples of this would be blending “smoke” and “fog” to get “smog” and “spoon” and “fork” to get “spork”. 

Formation 2 is when two words are blended around a common sequence of sounds, also known as blends with overlap. 
The first case of this formation involves clipping, where the words are clipped around the shared sound and then combined. An example of this is “lamb” and “hamburger” to get “lamburger”. In this case, the ‘h’ in “hamburger” is clipped to form the resulting blend. 
The second case of formation 2 is when the overlap preserves both words entirely and no clipping is involved. The reason no clipping is involved is because the overlapping letters are at the end of the first word and at the beginning of the second word. An example of this is “Africa” and “car” to get the new word “Africar”. When blended, the new word preserves the entirety of both the original words. Another example is “alcohol” and “holiday” to get “alcoholiday”. 

Formation 3 is when one word maintains its entire form in the blend, while the other word is clipped. An example of this formation is “mock” and “cocktail” to get “mocktail”. The entire word ‘mock’ is preserved and it is blended with the end of the second word. This formation applies in either direction. In the example “alphanumeric”, the first part of “alphabet” is blended with the entire word “numeric”. Our code was designed using these formations as guidelines. 




