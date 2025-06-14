README
======

This file briefly describes the contents of the public distribution
of the database called DIHANA.

The DIHANA corpus was supported by CICYT ("Comisión Interministerial
de Ciencia y Tecnología") of Spanish Government under project
TIC2002-04103-C03.  This project was carried out by a consortium
formed by Universidad de Zaragoza, Universidad del País Vasco and
Universitat Politècnica de València (coordinating entity).

DIHANA is composed of 900 human-computer dialogues in Spanish. The
acquisition of the DIHANA corpus was carried out by means of an
initial prototype using the Wizard of Oz technique. The operator
simulates speech recognition and understanding errors and the answers
being synthesized according to a predefined set of templates.  This
acquisition was only restricted at the semantical level (i.e., the
acquired dialogues are related to a specific task domain) and was not
restricted at the lexical and syntactical level (spontaneous
speech). In the acquisition process, this semantic control was
provided by the definition of scenarios that the user must accomplish
and by the wizard strategy, which defines the behavior of the
acquisition system.

The DIHANA task consists of the retrieval of information about Spanish
nationwide trains by telephone. Several types of scenarios were
defined in order to control the interaction of the user with the
system. A scenario is defined by: an objective, the information needed
by the user; a situation, the specific circumstances related to the
trip request; and the specific requirements of the trip, type of trip,
departure city, destination city, and one or more restrictions.

The DIHANA corpus contains 5.5 hours of spontaneous speech
corresponding to 6278 sentences. In total 225 speakers (153 males and
72 females) recorded 900 dialogues, resulting in 6,278 user
turns. Along with the dialogues (speech signals), their full
transcript is also provided and a lexicon phonetically containing all
the words pronounced in the database. In addition a semantic tagging
of the corpus and a labeling of the same corpus in terms of dialog
acts is also provided.

A more detailed description of DIHANA can be found in the "doc"
subfolder and in the following papers:

- N. Alcacer, J.M. Benedí, F. Blat, R. Granell, D. Martínez-Hinarejos
  and F. Torres: "Acquisition and Labelling of a Spontaneous Speech
  Dialogue Corpus". In proceedings of SPECOM, pages 583-586. Patras
  (Greece), October 2005.

- J.M. Benedí E.Lleida, A. Varona, M.J.Castro, I.Galiano, R.Justo,
  I. López, and A. Miguel: "Design and acquisition of a telephone
  spontaneous speech dialogue corpus in spanish: DIHANA". In
  proceedings of LREC, pages 1636-1639, Genova, Italy, May 2006.

Next we describe the contents of each subfolder:

README		 This file.

data		 The database: 75 speakers of 3 sites (Basque Country, 
		 Aragon and Valencian Country) for 4 scenarios making a 
                 total of 225 speakers (153 males and 72 females) with 
                 900 dialogues.

		 For each dialog is provided:

		 - the speech signal of each user turn (*.ul)
		 - the intermediate (*.dis) and final (*.xml) transcriptions
		 - the dialogue Act annotation

		   + Dialogue Act annotation on transcription (*.dia)
		   + Dialogue Act annotation on categorised transcription, 
		     without words for each category (*.cad)
		   + Dialogue Act annotation on categorised transcription, 
		     with words for each category (*.cwd)

semdata		 Semantic tagging of the full corpora, in the "data" subfolder, 
		 and documentation describing the process of semátinco labeling, 
		 in the "doc" folder. 

doc		 Various documents (PDF) related to the design and acquisition 
                 processes, the annotation format and event statistics.

guides		 5 lists of 45 speakers, which account for 5 leaving-one-out 
         	 partitions. One of the lists can be alternatively chosen as 
		 the test set, the other four joined to form the training set. 
		 Under the folder corresponding to each speaker, the speech 
		 signals and transcriptions corresponding to four dialogues 
		 can be found, so each partition consists of 720 training 
		 dialogues an 180 test dialogues.
--------------------------------------------------------------------------------
