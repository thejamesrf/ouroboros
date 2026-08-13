package game;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Handles saving and loading player progress in Hidden Gods.
 * Uses Java's Serialization to save/load the Player object to/from a file.
 */
public class SaveSystem {
    private static final String SAVE_DIR = "saves";

    /**
     * Saves the player's state to a file.
     * @param player The player to save.
     * @param filename The name of the save file (without extension).
     */
    public static void savePlayer(Player player, String filename) {
        try {
            // Create the saves directory if it doesn't exist
            Path saveDirPath = Paths.get(SAVE_DIR);
            if (!Files.exists(saveDirPath)) {
                Files.createDirectories(saveDirPath);
            }

            // Save the player object
            String filepath = SAVE_DIR + File.separator + filename + ".ser";
            FileOutputStream fileOut = new FileOutputStream(filepath);
            ObjectOutputStream out = new ObjectOutputStream(fileOut);
            out.writeObject(player);
            out.close();
            fileOut.close();
            System.out.println("✅ Game saved to " + filepath);
        } catch (IOException e) {
            System.out.println("❌ Error saving game: " + e.getMessage());
        }
    }

    /**
     * Loads a player's state from a file.
     * @param filename The name of the save file (without extension).
     * @return The loaded Player object, or null if loading fails.
     */
    public static Player loadPlayer(String filename) {
        try {
            String filepath = SAVE_DIR + File.separator + filename + ".ser";
            FileInputStream fileIn = new FileInputStream(filepath);
            ObjectInputStream in = new ObjectInputStream(fileIn);
            Player player = (Player) in.readObject();
            in.close();
            fileIn.close();
            System.out.println("✅ Game loaded from " + filepath);
            return player;
        } catch (FileNotFoundException e) {
            System.out.println("❌ Save file not found: " + e.getMessage());
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("❌ Error loading game: " + e.getMessage());
        }
        return null;
    }

    /**
     * Lists all available save files.
     * @return A list of save file names (without extensions).
     */
    public static List<String> listSaves() {
        List<String> saves = new ArrayList<>();
        File dir = new File(SAVE_DIR);
        if (dir.exists()) {
            File[] files = dir.listFiles((d, name) -> name.endsWith(".ser"));
            if (files != null) {
                for (File file : files) {
                    saves.add(file.getName().replace(".ser", ""));
                }
            }
        }
        return saves;
    }

    /**
     * Prints all available save files to the console.
     */
    public static void printSaves() {
        List<String> saves = listSaves();
        if (saves.isEmpty()) {
            System.out.println("No saved games found.");
        } else {
            System.out.println("\n=== SAVED GAMES ===");
            for (int i = 0; i < saves.size(); i++) {
                System.out.println((i + 1) + ". " + saves.get(i));
            }
        }
    }

    /**
     * Deletes a save file.
     * @param filename The name of the save file (without extension).
     * @return true if the file was deleted, false otherwise.
     */
    public static boolean deleteSave(String filename) {
        try {
            String filepath = SAVE_DIR + File.separator + filename + ".ser";
            File file = new File(filepath);
            if (file.exists()) {
                return file.delete();
            }
        } catch (Exception e) {
            System.out.println("❌ Error deleting save: " + e.getMessage());
        }
        return false;
    }
}
