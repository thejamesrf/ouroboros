package game;

import java.util.Arrays;
import java.util.List;

/**
 * Playbooks are character archetypes in Hidden Gods.
 * Each playbook has unique stats, moves, and a backstory.
 * Inspired by PbtA playbooks and Jungian archetypes.
 */
public enum Playbook {
    HACKER(
        "The Hacker",
        "You see the code beneath reality. Glitches are your playground.",
        new int[]{2, 0, 1, 0, -1}, // Weird, Cool, Sharp, Hot, Charm
        Arrays.asList("Hack the Code", "Glitch Out", "Introspect"),
        "You once rewrote the rules of a simulation layer to save a friend. The system still bears your fingerprints."
    ),
    GLITCH(
        "The Glitch",
        "You are a living anomaly. Reality bends around you, often against your will.",
        new int[]{0, -1, 0, 2, 1}, // Weird, Cool, Sharp, Hot, Charm
        Arrays.asList("Glitch Out", "Layer Hop", "Negotiate with a God"),
        "You don't remember a time when you weren't breaking things. The simulation fears you."
    ),
    ARCHITECT(
        "The Architect",
        "You build layers and shape reality. Order is your creed.",
        new int[]{1, 1, 2, -1, 0}, // Weird, Cool, Sharp, Hot, Charm
        Arrays.asList("Hack the Code", "Layer Hop", "Introspect"),
        "You designed a layer so perfect that even you couldn't escape it. Then you did."
    ),
    // Additional playbooks for future expansion
    SHADOW(
        "The Shadow",
        "You are the part of others they try to hide. You thrive in the unseen.",
        new int[]{1, -1, 1, 1, 0}, // Weird, Cool, Sharp, Hot, Charm
        Arrays.asList("Glitch Out", "Introspect", "Negotiate with a God"),
        "You were cast out of the light, but the dark is where the truth hides."
    ),
    SAGE(
        "The Sage",
        "You seek knowledge above all else. The simulation's secrets are your prize.",
        new int[]{0, 1, 2, 0, -1}, // Weird, Cool, Sharp, Hot, Charm
        Arrays.asList("Introspect", "Hack the Code", "Layer Hop"),
        "You've read every book in the Dream Layer's library. Some of them read you back."
    );

    private final String name;
    private final String description;
    private final int[] statModifiers; // [Weird, Cool, Sharp, Hot, Charm]
    private final List<String> moves;
    private final String backstory;

    Playbook(String name, String description, int[] statModifiers, List<String> moves, String backstory) {
        this.name = name;
        this.description = description;
        this.statModifiers = statModifiers;
        this.moves = moves;
        this.backstory = backstory;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public int[] getStatModifiers() {
        return statModifiers;
    }

    public List<String> getMoves() {
        return moves;
    }

    public String getBackstory() {
        return backstory;
    }

    /**
     * Gets the stat modifier for a specific stat.
     */
    public int getStatModifier(String statName) {
        switch (statName.toLowerCase()) {
            case "weird": return statModifiers[0];
            case "cool": return statModifiers[1];
            case "sharp": return statModifiers[2];
            case "hot": return statModifiers[3];
            case "charm": return statModifiers[4];
            default: return 0;
        }
    }

    /**
     * Prints all available playbooks for selection.
     */
    public static void printPlaybooks() {
        System.out.println("\n=== PLAYBOOKS ===");
        System.out.println("Choose your archetype:");
        int index = 1;
        for (Playbook playbook : values()) {
            System.out.printf("%d. %s: %s\n", index++, playbook.name, playbook.description);
        }
    }

    /**
     * Gets a playbook by its index (1-based).
     */
    public static Playbook getByIndex(int index) {
        if (index >= 1 && index <= values().length) {
            return values()[index - 1];
        }
        return HACKER; // Default to Hacker if invalid
    }

    @Override
    public String toString() {
        return String.format(
            "%s\n" +
            "- Description: %s\n" +
            "- Stats: Weird=%d, Cool=%d, Sharp=%d, Hot=%d, Charm=%d\n" +
            "- Moves: %s\n" +
            "- Backstory: %s",
            name, description,
            statModifiers[0], statModifiers[1], statModifiers[2], statModifiers[3], statModifiers[4],
            String.join(", ", moves),
            backstory
        );
    }
}
