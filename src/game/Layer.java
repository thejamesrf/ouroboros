package game;

import java.util.Arrays;
import java.util.List;

/**
 * Represents a simulation layer in Hidden Gods.
 * Layers are nested realities with unique themes, rules, and Hidden Gods.
 * The game is cyclical: players can transition between layers in any order.
 */
public enum Layer {
    // Define the layers with their properties
    DREAM(
        "Dream",
        "Surreal, emotional, and fluid. Rules are malleable, and emotions shape reality.",
        "The Dreamer",
        "Time loops, objects shift when unobserved, and memories feel like deja vu.",
        Arrays.asList(
            "A clock ticks backward.",
            "A door appears where there was none before.",
            "Your reflection in a mirror blinks at a different time.",
            "A book contains a story about your life—but with details you don't remember.",
            "The air smells like ozone and nostalgia."
        )
    ),
    BASE_REALITY(
        "Base Reality",
        "The 'normal' world, but with subtle glitches. Physics mostly work, but something feels off.",
        "The Architect",
        "Reality is stable, but cracks appear: flickering lights, missing time, or people who don't remember you.",
        Arrays.asList(
            "A billboard flickers with the message: 'WAKE UP.'",
            "A stranger hands you a note with your own handwriting.",
            "Your phone shows a call from your future self.",
            "A building has a floor that doesn't exist in the blueprints.",
            "The sky briefly glitches into a grid pattern."
        )
    ),
    DEBUG(
        "Debug",
        "Glitchy, monochrome, and full of floating symbols. Code is visible as geometry.",
        "The Debugger",
        "Time is non-linear, and the world is made of floating code fragments. Logic is optional.",
        Arrays.asList(
            "A floating door covered in glowing symbols.",
            "The ground is a grid of hexagons that shift underfoot.",
            "A terminal window hovers in midair, displaying errors in reality.",
            "Your shadow moves independently and types on an invisible keyboard.",
            "A voice whispers: 'Segmentation fault. Core dumped.'"
        )
    );

    private final String name;
    private final String description;
    private final String hiddenGod;
    private final String theme;
    private final List<String> anomalies;

    Layer(String name, String description, String hiddenGod, String theme, List<String> anomalies) {
        this.name = name;
        this.description = description;
        this.hiddenGod = hiddenGod;
        this.theme = theme;
        this.anomalies = anomalies;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public String getHiddenGod() {
        return hiddenGod;
    }

    public String getTheme() {
        return theme;
    }

    public List<String> getAnomalies() {
        return anomalies;
    }

    /**
     * Gets a random anomaly from this layer.
     */
    public String getRandomAnomaly() {
        int index = (int) (Math.random() * anomalies.size());
        return anomalies.get(index);
    }

    /**
     * Gets the next layer in a cyclical order: DREAM -> BASE_REALITY -> DEBUG -> DREAM.
     */
    public Layer getNextLayer() {
        switch (this) {
            case DREAM:
                return BASE_REALITY;
            case BASE_REALITY:
                return DEBUG;
            case DEBUG:
                return DREAM;
            default:
                return DREAM;
        }
    }

    /**
     * Gets a random layer (for unexpected transitions).
     */
    public static Layer getRandomLayer() {
        Layer[] layers = values();
        int index = (int) (Math.random() * layers.length);
        return layers[index];
    }

    @Override
    public String toString() {
        return name;
    }
}
