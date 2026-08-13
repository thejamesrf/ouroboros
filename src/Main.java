import game.*;
import story.Story;
import java.util.Scanner;

/**
 * Hidden Gods: A Java RPG about nested simulations, glitches, and Hidden Gods.
 * 
 * The game starts in the Dream Layer, where players encounter anomalies and
 * use PbtA-style moves (Roll+Stat) to navigate the cyclical layers (Dream -> Base Reality -> Debug -> Dream).
 * 
 * Features:
 * - Playbooks: Choose from The Hacker, The Glitch, or The Architect.
 * - Save/Load: Save your progress and continue later.
 * - ASCII Art: Visual flair for layers, anomalies, and gods.
 * - Cyclical Win Condition: Complete the cycle to retain a piece of "self" and start anew.
 * 
 * Themes:
 * - Simulation Hypothesis: Reality is a stack of simulations.
 * - Jungian Archetypes & IFS: Characters are shaped by inner parts.
 * - Cyclical Layers: Players transition between layers in a loop.
 * - Ouroboros: The cycle is eternal; the player retains memories/stats between cycles.
 */
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Print ASCII logo
        AsciiArt.printLogo();
        System.out.println("A game about nested simulations and the gods who shape reality.");
        AsciiArt.printDivider();

        // Playbook selection
        Playbook playbook = selectPlaybook(scanner);

        // Player name
        System.out.print("Enter your name: ");
        String playerName = scanner.nextLine();

        // Start in the Dream Layer (players won't know it's a dream at first)
        Player player = new Player(playerName, Layer.DREAM, playbook);
        Story story = new Story(player, scanner);

        // Print playbook info
        System.out.println("\n" + AsciiArt.BOLD_DIVIDER);
        AsciiArt.printPlaybookIcon(playbook);
        System.out.println("You are: " + playbook.getName());
        System.out.println(playbook.getDescription());
        System.out.println("Backstory: " + playbook.getBackstory());
        System.out.println(AsciiArt.BOLD_DIVIDER);

        story.start();

        // Main game loop
        boolean playing = true;
        while (playing) {
            System.out.println("\n" + AsciiArt.DIVIDER);
            System.out.println("What would you like to do?");
            System.out.println("1. Explore (encounter an anomaly)");
            System.out.println("2. View stats");
            System.out.println("3. View discovered clues");
            System.out.println("4. View cycle info");
            System.out.println("5. Save game");
            System.out.println("6. Load game");
            System.out.println("7. Quit");
            System.out.print("> ");

            int choice;
            try {
                choice = scanner.nextInt();
                scanner.nextLine(); // Consume newline
            } catch (Exception e) {
                scanner.nextLine(); // Clear invalid input
                System.out.println("Invalid input. Please enter a number.");
                continue;
            }

            switch (choice) {
                case 1:
                    story.encounterAnomaly();
                    break;
                case 2:
                    story.showStats();
                    break;
                case 3:
                    story.showClues();
                    break;
                case 4:
                    story.showCycleInfo();
                    break;
                case 5:
                    saveGame(scanner, player);
                    break;
                case 6:
                    player = loadGame(scanner);
                    if (player != null) {
                        story = new Story(player, scanner);
                        System.out.println("Game loaded. Continuing adventure...");
                    }
                    break;
                case 7:
                    playing = false;
                    story.end();
                    break;
                default:
                    System.out.println("Invalid choice. Try again.");
            }
        }

        scanner.close();
    }

    /**
     * Lets the player select a playbook.
     */
    private static Playbook selectPlaybook(Scanner scanner) {
        AsciiArt.printTitle("SELECT YOUR PLAYBOOK");
        Playbook.printPlaybooks();
        System.out.print("Choose a playbook (1-5): ");

        int choice;
        try {
            choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline
        } catch (Exception e) {
            scanner.nextLine(); // Clear invalid input
            System.out.println("Invalid input. Defaulting to The Hacker.");
            return Playbook.HACKER;
        }

        return Playbook.getByIndex(choice);
    }

    /**
     * Saves the current game.
     */
    private static void saveGame(Scanner scanner, Player player) {
        System.out.print("Enter a name for your save file: ");
        String filename = scanner.nextLine();
        SaveSystem.savePlayer(player, filename);
    }

    /**
     * Loads a saved game.
     */
    private static Player loadGame(Scanner scanner) {
        SaveSystem.printSaves();
        if (SaveSystem.listSaves().isEmpty()) {
            return null;
        }
        System.out.print("Enter the name of the save file to load: ");
        String filename = scanner.nextLine();
        return SaveSystem.loadPlayer(filename);
    }
}
