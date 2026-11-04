JAVA=java
JAVAC=javac
JFLEX=$(JAVA) -jar jflex-full-1.8.2.jar
CUPJAR=./java-cup-11b.jar
CUP=$(JAVA) -jar $(CUPJAR)
CP=.:$(CUPJAR)

TESTDIR = testfiles
TESTS   = $(basename $(notdir $(wildcard $(TESTDIR)/*.txt)))

NETID = kxv220016
NAME  = ky-anh-vo
PKG   = project01-$(NETID)-$(NAME)

default: run

.SUFFIXES: $(SUFFIXES) .class .java

.java.class:
		$(JAVAC) -cp $(CP) $*.java

FILE=    Lexer.java      parser.java    sym.java \
    LexerTest.java

run: basicTest.txt

.PHONY: default run all clean test submit

test: all
	@for t in $(TESTS); do \
		echo "=== $$t ==="; \
		$(JAVA) -cp $(CP) LexerTest $(TESTDIR)/$$t.txt > $$t-output.txt; \
		cat $$t-output.txt; \
	done

submit: clean test
	tar -cJf $(PKG).tar.xz \
		tokens.jflex grammar.cup Makefile LexerTest.java README.md \
		*.jar testfiles *-output.txt
	@echo "Created $(PKG).tar.xz"

all: Lexer.java parser.java $(FILE:java=class)

basicTest.txt: all
		$(JAVA) -cp $(CP) LexerTest basicTest.txt > basicTest-output.txt
		cat basicTest.txt
		cat -n basicTest-output.txt

clean:
		rm -f *.class *~ *.bak Lexer.java parser.java sym.java *-output.txt

Lexer.java: tokens.jflex
		$(JFLEX) tokens.jflex

parser.java: grammar.cup
		$(CUP) -interface < grammar.cup

parserD.java: grammar.cup
		$(CUP) -interface -dump < grammar.cup
