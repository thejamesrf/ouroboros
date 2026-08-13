package game;

import java.util.Arrays;
import java.util.List;

/**
 * Represents an anomaly in Hidden Gods.
 * Anomalies are glitches, clues, or disruptions in the simulation that hint at other layers.
 */
public class Anomaly {
    private final String name;
    private final String manifestation;
    private final String clue;
    private final String purpose;
    private final String risk;
    private final Layer layer;

    public Anomaly(String name, String manifestation, String clue, String purpose, String risk, Layer layer) {
        this.name = name;
        this.manifestation = manifestation;
        this.clue = clue;
        this.purpose = purpose;
        this.risk = risk;
        this.layer = layer;
    }

    public String getName() {
        return name;
    }

    public String getManifestation() {
        return manifestation;
    }

    public String getClue() {
        return clue;
    }

    public String getPurpose() {
        return purpose;
    }

    public String getRisk() {
        return risk;
    }

    public Layer getLayer() {
        return layer;
    }

    /**
     * Generates a random anomaly for the given layer.
     */
    public static Anomaly generateRandomAnomaly(Layer layer) {
        List<Anomaly> anomalies = getAnomaliesForLayer(layer);
        int index = (int) (Math.random() * anomalies.size());
        return anomalies.get(index);
    }

    /**
     * Defines anomalies for each layer.
     */
    private static List<Anomaly> getAnomaliesForLayer(Layer layer) {
        switch (layer) {
            case DREAM:
                return Arrays.asList(
                    new Anomaly(
                        "The Echoing Door",
                        "A door that repeats the last 3 seconds of sound when opened.",
                        "The air smells like ozone.",
                        "To test your perception of time.",
                        "Roll+Weird to resist disorientation (2-Weird).",
                        Layer.DREAM
                    ),
                    new Anomaly(
                        "The Backward Clock",
                        "A clock with hands moving counterclockwise.",
                        "Time feels like it's looping.",
                        "To reveal the fluidity of time in this layer.",
                        "Roll+Sharp to understand its meaning.",
                        Layer.DREAM
                    ),
                    new Anomaly(
                        "The Shifting Library",
                        "A library where books rearrange themselves when unobserved.",
                        "You recall a book that wasn't here before.",
                        "To challenge your memory of reality.",
                        "Roll+Cool to navigate without getting lost.",
                        Layer.DREAM
                    )
                );
            case BASE_REALITY:
                return Arrays.asList(
                    new Anomaly(
                        "The Flickering Billboard",
                        "A billboard that flickers with cryptic messages.",
                        "The message reads: 'WAKE UP.'",
                        "To hint at the simulation's true nature.",
                        "Roll+Sharp to decipher the message.",
                        Layer.BASE_REALITY
                    ),
                    new Anomaly(
                        "The Stranger's Note",
                        "A stranger hands you a note written in your own handwriting.",
                        "The note says: 'You are not who you think you are.'",
                        "To plant doubt about your identity.",
                        "Roll+Weird to resist the cognitive dissonance.",
                        Layer.BASE_REALITY
                    ),
                    new Anomaly(
                        "The Missing Floor",
                        "A building with a floor that doesn't exist in the blueprints.",
                        "The elevator buttons include a floor labeled 'DEBUG'.",
                        "To reveal the layers beneath reality.",
                        "Roll+Cool to investigate without drawing attention.",
                        Layer.BASE_REALITY
                    )
                );
            case DEBUG:
                return Arrays.asList(
                    new Anomaly(
                        "The Floating Door",
                        "A door covered in glowing symbols, floating in midair.",
                        "The symbols resemble code.",
                        "To allow transition to another layer.",
                        "Roll+Weird to hack the door open.",
                        Layer.DEBUG
                    ),
                    new Anomaly(
                        "The Hex Grid",
                        "The ground is a grid of hexagons that shift underfoot.",
                        "The grid pulses with a rhythm like a heartbeat.",
                        "To test your ability to navigate non-Euclidean space.",
                        "Roll+Cool to avoid falling through the grid.",
                        Layer.DEBUG
                    ),
                    new Anomaly(
                        "The Terminal Window",
                        "A terminal window hovers in midair, displaying errors in reality.",
                        "The last line reads: 'Segmentation fault. Core dumped.'",
                        "To reveal the layer's code-like nature.",
                        "Roll+Sharp to interpret the errors.",
                        Layer.DEBUG
                    )
                );
            default:
                return Arrays.asList();
        }
    }

    @Override
    public String toString() {
        return String.format(
            "🔍 %s\n" +
            "- Manifestation: %s\n" +
            "- Clue: %s\n" +
            "- Purpose: %s\n" +
            "- Risk: %s",
            name, manifestation, clue, purpose, risk
        );
    }
}
