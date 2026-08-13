package game;

import java.util.Random;

/**
 * Utility class for rolling dice in Hidden Gods (PbtA-style).
 * Simulates 2d6 + stat rolls for moves like "Hack the Code" or "Layer Hop".
 */
public class Dice {
    private static final Random random = new Random();

    /**
     * Rolls 2d6 and returns the total (2-12).
     */
    public static int roll2d6() {
        return random.nextInt(6) + 1 + random.nextInt(6) + 1;
    }

    /**
     * Rolls 2d6 + stat and returns the total.
     * @param stat The stat value to add (e.g., Weird, Cool, Sharp).
     */
    public static int rollPlusStat(int stat) {
        return roll2d6() + stat;
    }

    /**
     * Determines if a roll is a success (6+), partial success (4-5), or failure (2-3).
     * In PbtA, 6+ is a success, 4-5 is a partial success, and 2-3 is a failure.
     */
    public static String getResult(int roll) {
        if (roll >= 6) {
            return "Success!";
        } else if (roll >= 4) {
            return "Partial Success.";
        } else {
            return "Failure.";
        }
    }

    /**
     * Simulates a move roll (e.g., "Roll+Weird").
     * @param statName The name of the stat (e.g., "Weird", "Cool").
     * @param statValue The value of the stat.
     * @return A formatted string with the roll result.
     */
    public static String rollMove(String statName, int statValue) {
        int roll = rollPlusStat(statValue);
        int diceRoll = roll - statValue; // Extract just the 2d6 part for display
        return String.format("Rolling 2d6 + %s (%d)... Result: %d (%s)", 
                statName, statValue, roll, getResult(roll));
    }
}
