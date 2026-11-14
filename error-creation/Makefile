JAVA=java
JAVAC=javac
JFLEX=$(JAVA) -jar jflex-full-1.8.2.jar
CUPJAR=./java-cup-11b.jar
CUP=$(JAVA) -jar $(CUPJAR)

# Both phases share the lexer, the driver and the AST. Only the grammar differs,
# so each one is generated and compiled into its own directory.
BUILD = build
AST   = $(wildcard ast/*.java)

NETID = kxv220016
NAME  = ky-anh-vo
PKG   = project02-$(NETID)-$(NAME)

PHASE ?= 2

.PHONY: default all phase1 phase2 run test submit clean

default: all

all: phase1 phase2

phase1: $(BUILD)/phase1/.compiled
phase2: $(BUILD)/phase2/.compiled

# Usage: make run PHASE=1 FILE=Phase1Tests/Phase1_statements.txt
run: phase$(PHASE)
	@$(JAVA) -cp $(BUILD)/phase$(PHASE):$(CUPJAR) ScannerTest $(FILE)

test: all
	@for p in 1 2; do \
		mkdir -p results/phase$$p; \
		for f in Phase$${p}Tests/*.txt; do \
			out=results/phase$$p/$$(basename $$f .txt)-output.txt; \
			echo "=== $$f ==="; \
			$(JAVA) -cp $(BUILD)/phase$$p:$(CUPJAR) ScannerTest $$f > $$out; \
			cat $$out; echo; \
		done; \
	done

submit: clean test
	tar -cJf $(PKG).tar.xz \
		tokens.jflex phase1 phase2 ast ScannerTest.java Makefile README.md errors_and_solutions.pdf \
		*.jar Phase1Tests/*.txt Phase2Tests/*.txt example_input.txt example_output-1.txt results
	@echo "Created $(PKG).tar.xz"

clean:
	rm -rf $(BUILD) results

$(BUILD)/%/parser.java: %/grammar.cup
	@mkdir -p $(@D)
	$(CUP) -interface -destdir $(@D) $<

$(BUILD)/%/Lexer.java: tokens.jflex
	@mkdir -p $(@D)
	$(JFLEX) --nobak -d $(@D) $<

$(BUILD)/%/.compiled: $(BUILD)/%/parser.java $(BUILD)/%/Lexer.java ScannerTest.java $(AST)
	$(JAVAC) --release 11 -cp $(CUPJAR) -d $(@D) $(@D)/parser.java $(@D)/sym.java $(@D)/Lexer.java ScannerTest.java $(AST)
	@touch $@

.PRECIOUS: $(BUILD)/%/parser.java $(BUILD)/%/Lexer.java
