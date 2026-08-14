package story;

import game.*;
import java.util.Scanner;

/**
 * Manages the narrative flow of Hidden Gods.
 * Handles layer transitions, anomaly encounters, Hidden God interactions, and cyclical win conditions.
 */
public class Story {
    private Player player;
    private Scanner scanner;

    public Story(Player player, Scanner scanner) {
        this.player = player;
        this.scanner = scanner;
    }

    /**
     * Starts the game and introduces the player to the current layer.
     */
    public void start() {
        System.out.println("\n" + AsciiArt.BOLD_DIVIDER);
        System.out.println("You find yourself in a strange place...");
        describeCurrentLayer();
    }

    /**
     * Describes the player's current layer with ASCII art.
     */
    public void describeCurrentLayer() {
        Layer currentLayer = player.getCurrentLayer();
        AsciiArt.printLayer(currentLayer);
        System.out.println("🌌 You are in the " + currentLayer.getName() + " Layer.");
        System.out.println(currentLayer.getDescription());
        System.out.println(currentLayer.getTheme());
    }

    /**
     * Presents an anomaly to the player and handles their response.
     */
    public void encounterAnomaly() {
        Layer currentLayer = player.getCurrentLayer();
        Anomaly anomaly = Anomaly.generateRandomAnomaly(currentLayer);

        // Print anomaly ASCII art if available
        AsciiArt.printAnomaly(anomaly.getName().toLowerCase());

        System.out.println("\n🔍 " + anomaly.getName());
        System.out.println("🎭 Manifestation: " + anomaly.getManifestation());
        System.out.println("🔍 Clue: " + anomaly.getClue());
        player.addClue(anomaly.getClue());

        System.out.println("\nWhat do you do?");
        // Show playbook-specific moves if available
        List<String> moves = player.getPlaybook().getMoves();
        for (int i = 0; i < moves.size(); i++) {
            System.out.println((i + 1) + ". " + moves.get(i) + " (Roll+" + getStatForMove(moves.get(i)) + ")");
        }
        // Show all moves if playbook moves are not enough
        if (moves.size() < 4) {
            if (!moves.contains("Hack the Code")) {
                System.out.println((moves.size() + 1) + ". Hack the Code (Roll+Weird)");
            }
            if (!moves.contains("Introspect")) {
                System.out.println((moves.size() + 2) + ". Introspect (Roll+Sharp)");
            }
            if (!moves.contains("Layer Hop")) {
                System.out.println((moves.size() + 3) + ". Layer Hop (Roll+Cool)");
            }
            if (!moves.contains("Negotiate with a God")) {
                System.out.println((moves.size() + 4) + ". Negotiate with a God (Roll+Charm)");
            }
        }
        System.out.println((moves.size() + 5) + ". Do nothing");
        System.out.print("> ");

        int choice;
        try {
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline
        } catch (Exception e) {
            scanner.nextLine(); // Clear invalid input
            System.out.println("Invalid input. The anomaly fades away.");
            return;
        }

        // Handle playbook moves
        if (choice >= 1 && choice <= moves.size()) {
            String move = moves.get(choice - 1);
            handleMove(move, getStatForMove(move));
        } else if (choice == moves.size() + 1) {
            handleMove("Hack the Code", "Weird");
        } else if (choice == moves.size() + 2) {
            handleMove("Introspect", "Sharp");
        } else if (choice == moves.size() + 3) {
            handleLayerHop();
        } else if (choice == moves.size() + 4) {
            handleNegotiateWithGod();
        } else if (choice == moves.size() + 5) {
            System.out.println("You hesitate. The anomaly lingers...");
        } else {
            System.out.println("Invalid choice. The anomaly fades away.");
        }

        // Check for win condition after every action
        checkWinCondition();
    }

    /**
     * Gets the stat associated with a move.
     */
    private String getStatForMove(String move) {
        switch (move) {
            case "Hack the Code": return "Weird";
            case "Layer Hop": return "Cool";
            case "Introspect": return "Sharp";
            case "Glitch Out": return "Hot";
            case "Negotiate with a God": return "Charm";
            default: return "Weird";
        }
    }

    /**
     * Handles a move (e.g., Hack the Code, Introspect).
     */
    private void handleMove(String moveName, String statName) {
        String result = player.performMove(moveName, statName);
        System.out.println(result);

        // Determine outcome based on the roll
        int roll = extractRollValue(result);
        if (roll >= 6) {
            System.out.println("The anomaly responds to your action!");
            // Reveal a clue or transition layers
            if (Math.random() > 0.5) {
                Layer nextLayer = player.getCurrentLayer().getNextLayer();
                System.out.println("A portal to the " + nextLayer.getName() + " Layer opens!");
                player.setCurrentLayer(nextLayer);
                describeCurrentLayer();
            } else {
                System.out.println("You gain a deeper understanding of this layer.");
            }
        } else if (roll >= 4) {
            System.out.println("The anomaly resists, but you learn something.");
            System.out.println("Clue: " + player.getCurrentLayer().getRandomAnomaly());
        } else {
            System.out.println("The anomaly backfires! You feel disoriented.");
            // Optional: Apply a penalty or trigger a Hidden God encounter
            if (Math.random() > 0.7) {
                encounterHiddenGod();
            }
        }
    }

    /**
     * Handles the Layer Hop move.
     */
    private void handleLayerHop() {
        String result = player.performMove("Layer Hop", "Cool");
        System.out.println(result);

        int roll = extractRollValue(result);
        if (roll >= 6) {
            // Move to the next layer in the cycle
            Layer nextLayer = player.getCurrentLayer().getNextLayer();
            System.out.println("You successfully transition to the " + nextLayer.getName() + " Layer!");
            player.setCurrentLayer(nextLayer);
            describeCurrentLayer();
        } else if (roll >= 4) {
            // Move to a random layer (partial success)
            Layer randomLayer = Layer.getRandomLayer();
            System.out.println("You stumble into the " + randomLayer.getName() + " Layer!");
            player.setCurrentLayer(randomLayer);
            describeCurrentLayer();
        } else {
            System.out.println("You fail to transition and remain in the " + player.getCurrentLayer().getName() + " Layer.");
        }
    }

    /**
     * Handles the Negotiate with a God move.
     */
    private void handleNegotiateWithGod() {
        String result = player.performMove("Negotiate with a God", "Charm");
        System.out.println(result);

        int roll = extractRollValue(result);
        if (roll >= 6) {
            encounterHiddenGod();
        } else if (roll >= 4) {
            System.out.println("A Hidden God acknowledges you but offers no help.");
        } else {
            System.out.println("The Hidden God ignores you. You feel a sense of dread.");
        }
    }

    /**
     * Encounters a Hidden God in the current layer.
     */
    private void encounterHiddenGod() {
        Layer currentLayer = player.getCurrentLayer();
        HiddenGod god = HiddenGod.getGodForLayer(currentLayer);

        // Print god ASCII art
        AsciiArt.printHiddenGod(god);

        System.out.println("\n" + god.getRandomDialogue());
        System.out.println("The " + god.getName() + " offers a bargain: " + god.getBargain());
        System.out.println("1. Accept the bargain");
        System.out.println("2. Decline");
        System.out.print("> ");

        int choice;
        try {
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline
        } catch (Exception e) {
            scanner.nextLine(); // Clear invalid input
            System.out.println("Invalid input. The god vanishes.");
            return;
        }

        if (choice == 1) {
            System.out.println("You accept the bargain. The " + god.getName() + " smiles.");
            // Reward: Gain a clue or stat boost
            player.addClue("Bargain with " + god.getName());
            player.incrementStat("Charm");
            System.out.println("You feel more confident. (+1 Charm)");
        } else {
            System.out.println("You decline. The " + god.getName() + " vanishes, displeased.");
        }
    }

    /**
     * Checks if the player has completed the win condition (visited all layers + found the final clue).
     * If so, starts a new cycle with retained memories/stats.
     */
    private void checkWinCondition() {
        player.checkAllLayersVisited();
        if (player.hasVisitedAllLayers()) {
            // Check if player has the final clue (e.g., "The cycle is eternal")
            boolean hasFinalClue = player.getDiscoveredClues().stream()
                .anyMatch(clue -> clue.toLowerCase().contains("cycle") || 
                                 clue.toLowerCase().contains("eternal") ||
                                 clue.toLowerCase().contains("ouroboros"));

            if (hasFinalClue) {
                System.out.println("\n" + AsciiArt.BOLD_DIVIDER);
                AsciiArt.printTitle("CYCLE COMPLETE");
                System.out.println("You have uncovered the truth: The simulation is cyclical.");
                System.out.println("The Hidden Gods whisper: 'The ouroboros eats its own tail.'");

                // Retain a piece of self
                player.retainBestStat();  // +1 to highest stat
                String lastClue = player.getDiscoveredClues().get(player.getDiscoveredClues().size() - 1);
                player.addRetainedMemory("Cycle " + player.getCycleCount() + ": \"" + lastClue + "\"");

                // Start a new cycle
                player.incrementCycle();
                player.setCurrentLayer(Layer.DREAM);  // Reset to Dream Layer
                System.out.println("\n✨ A new cycle begins... You retain a piece of your former self.");
                System.out.println("✨ +1 to your highest stat!");

                // Show retained memories
                if (!player.getRetainedMemories().isEmpty()) {
                    System.out.println("\n📜 Retained Memories:");
                    for (String mem : player.getRetainedMemories()) {
                        System.out.println("  - " + mem);
                    }
                }

                describeCurrentLayer();  // Restart in Dream Layer
            }
        }
    }

    /**
     * Extracts the roll value from a move result string.
     */
    private int extractRollValue(String result) {
        // Example: "Rolling 2d6 + Weird (1)... Result: 8 (Success!)"
        int start = result.indexOf("Result: ") + 8;
        int end = result.indexOf(" (", start);
        if (start > 7 && end > start) {
            return Integer.parseInt(result.substring(start, end));
        }
        return 0;
    }

    /**
     * Displays the player's discovered clues.
     */
    public void showClues() {
        if (player.getDiscoveredClues().isEmpty()) {
            System.out.println("You haven't discovered any clues yet.");
        } else {
            AsciiArt.printTitle("DISCOVERED CLUES");
            for (String clue : player.getDiscoveredClues()) {
                System.out.println("- " + clue);
            }
        }
    }

    /**
     * Displays the player's stats.
     */
    public void showStats() {
        AsciiArt.printTitle("PLAYER STATS");
        System.out.println(player.getStatsSummary());
    }

    /**
     * Displays cycle info (cycle count + retained memories).
     */
    public void showCycleInfo() {
        AsciiArt.printTitle("CYCLE INFO");
        System.out.println("🔄 Cycle: " + player.getCycleCount());
        if (!player.getRetainedMemories().isEmpty()) {
            System.out.println("\n📜 Retained Memories:");
            for (String memory : player.getRetainedMemories()) {
                System.out.println("  - " + memory);
            }
        } else {
            System.out.println("No memories retained yet.");
        }
    }

    /**
     * Ends the game and displays a summary.
     */
    public void end() {
        System.out.println("\n" + AsciiArt.BOLD_DIVIDER);
        AsciiArt.printTitle("GAME OVER");
        System.out.println("You have explored the following layers:");
        for (Layer layer : player.getVisitedLayers()) {
            System.out.println("- " + layer.getName());
        }
        System.out.println("\nFinal Stats:");
        System.out.println(player.getStatsSummary());
        System.out.println("\nTotal Cycles Completed: " + player.getCycleCount());
        System.out.println(AsciiArt.BOLD_DIVIDER);
    }
}
