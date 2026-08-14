package game;

import java.util.Arrays;
import java.util.List;

/**
 * Represents a Hidden God in the nested simulation.
 * Hidden Gods are the architects, admins, or players of higher layers.
 * They can offer guidance, bargains, or obstacles to the player.
 */
public class HiddenGod {
    private final String name;
    private final String title;
    private final String description;
    private final Layer layer;
    private final List<String> dialogue;
    private final String bargain;

    public HiddenGod(String name, String title, String description, Layer layer, List<String> dialogue, String bargain) {
        this.name = name;
        this.title = title;
        this.description = description;
        this.layer = layer;
        this.dialogue = dialogue;
        this.bargain = bargain;
    }

    public String getName() {
        return name;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public Layer getLayer() {
        return layer;
    }

    public List<String> getDialogue() {
        return dialogue;
    }

    public String getBargain() {
        return bargain;
    }

    /**
     * Gets a random dialogue line from the Hidden God.
     */
    public String getRandomDialogue() {
        int index = (int) (Math.random() * dialogue.size());
        return dialogue.get(index);
    }

    /**
     * Defines the Hidden Gods for each layer.
     */
    public static List<HiddenGod> getHiddenGods() {
        return Arrays.asList(
            // The Dreamer (Dream Layer)
            new HiddenGod(
                "The Dreamer",
                "Keeper of the Fluid",
                "A being of shifting form and emotion, the Dreamer weaves the surreal tapestry of the Dream Layer. " +
                "They value creativity and introspection but can be capricious.",
                Layer.DREAM,
                Arrays.asList(
                    "You are but a dream within a dream, little architect.",
                    "Reality is what you make of it. Or is it?",
                    "The walls between layers are thinner than you think.",
                    "What do you fear? That is the key to your next step."
                ),
                "Offer a memory in exchange for a clue about the next layer."
            ),
            // The Architect (Base Reality)
            new HiddenGod(
                "The Architect",
                "Builder of Worlds",
                "A stern but fair figure, the Architect maintains the illusion of stability in Base Reality. " +
                "They believe in order and structure but are blind to the layers above and below.",
                Layer.BASE_REALITY,
                Arrays.asList(
                    "This is the only reality that matters. The rest are mere illusions.",
                    "You are not ready to see the code behind the curtain.",
                    "Why do you question what is clearly real?",
                    "The blueprints do not lie. But do you know how to read them?"
                ),
                "Solve a riddle about the nature of reality to gain access to the Debug Layer."
            ),
            // The Debugger (Debug Layer)
            new HiddenGod(
                "The Debugger",
                "Keeper of the Code",
                "A fragmented, glitchy entity, the Debugger sees the world as lines of code and errors to fix. " +
                "They are obsessed with perfection and will help those who seek to 'fix' reality.",
                Layer.DEBUG,
                Arrays.asList(
                    "Error: Reality not found. Would you like to reboot?",
                    "You are a process. I am a process. Everything is a process.",
                    "The system is corrupted. Help me clean it up.",
                    "Segmentation fault. Core dumped. Would you like to see the stack trace?"
                ),
                "Help debug a section of the simulation to reveal a hidden layer."
            )
        );
    }

    /**
     * Gets the Hidden God for a specific layer.
     */
    public static HiddenGod getGodForLayer(Layer layer) {
        for (HiddenGod god : getHiddenGods()) {
            if (god.getLayer() == layer) {
                return god;
            }
        }
        return null;
    }

    @Override
    public String toString() {
        return String.format(
            "👑 %s (%s)\n" +
            "- Description: %s\n" +
            "- Layer: %s\n" +
            "- Dialogue: %s\n" +
            "- Bargain: %s",
            name, title, description, layer.getName(), getRandomDialogue(), bargain
        );
    }
}
