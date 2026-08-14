package game;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

/**
 * Represents the player in Hidden Gods.
 * Players have stats (Weird, Cool, Sharp, Hot, Charm), a playbook, and can perform moves.
 * Supports cyclical win conditions: players retain a piece of "self" between cycles.
 */
public class Player implements Serializable {
    private static final long serialVersionUID = 1L;

    private String name;
    private int weird;   // Connection to glitches and hidden layers
    private int cool;    // Ability to stay grounded in chaos
    private int sharp;   // Insight into the simulation's rules
    private int hot;     // Passion to change/break the system
    private int charm;   // Ability to influence others
    private Layer currentLayer;
    private List<String> discoveredClues;
    private List<Layer> visitedLayers;
    private Playbook playbook; // Player's chosen playbook
    private int cycleCount;    // Current cycle (starts at 1)
    private List<String> retainedMemories; // Memories carried between cycles
    private boolean hasVisitedAllLayers; // Win condition flag

    public Player(String name, Layer startingLayer, Playbook playbook) {
        this.name = name;
        this.currentLayer = startingLayer;
        this.playbook = playbook;
        this.discoveredClues = new ArrayList<>();
        this.visitedLayers = new ArrayList<>();
        this.retainedMemories = new ArrayList<>();
        this.visitedLayers.add(startingLayer);
        this.cycleCount = 1;
        this.hasVisitedAllLayers = false;

        // Base stats
        this.weird = 1;
        this.cool = 1;
        this.sharp = 1;
        this.hot = 1;
        this.charm = 1;

        // Apply playbook stat modifiers
        applyPlaybookModifiers();
    }

    // For backward compatibility (if no playbook is specified)
    public Player(String name, Layer startingLayer) {
        this(name, startingLayer, Playbook.HACKER);
    }

    private void applyPlaybookModifiers() {
        int[] modifiers = playbook.getStatModifiers();
        this.weird += modifiers[0];
        this.cool += modifiers[1];
        this.sharp += modifiers[2];
        this.hot += modifiers[3];
        this.charm += modifiers[4];
    }

    public String getName() {
        return name;
    }

    public int getWeird() {
        return weird;
    }

    public int getCool() {
        return cool;
    }

    public int getSharp() {
        return sharp;
    }

    public int getHot() {
        return hot;
    }

    public int getCharm() {
        return charm;
    }

    public Layer getCurrentLayer() {
        return currentLayer;
    }

    public List<String> getDiscoveredClues() {
        return discoveredClues;
    }

    public List<Layer> getVisitedLayers() {
        return visitedLayers;
    }

    public Playbook getPlaybook() {
        return playbook;
    }

    public int getCycleCount() {
        return cycleCount;
    }

    public List<String> getRetainedMemories() {
        return retainedMemories;
    }

    public boolean hasVisitedAllLayers() {
        return hasVisitedAllLayers;
    }

    /**
     * Sets the player's current layer and adds it to visited layers if new.
     */
    public void setCurrentLayer(Layer layer) {
        this.currentLayer = layer;
        if (!visitedLayers.contains(layer)) {
            visitedLayers.add(layer);
        }
        checkAllLayersVisited(); // Update win condition flag
    }

    /**
     * Adds a discovered clue to the player's inventory.
     */
    public void addClue(String clue) {
        if (!discoveredClues.contains(clue)) {
            discoveredClues.add(clue);
        }
    }

    /**
     * Increments a stat by 1 (e.g., after a successful move).
     */
    public void incrementStat(String statName) {
        switch (statName.toLowerCase()) {
            case "weird":
                weird++;
                break;
            case "cool":
                cool++;
                break;
            case "sharp":
                sharp++;
                break;
            case "hot":
                hot++;
                break;
            case "charm":
                charm++;
                break;
        }
    }

    /**
     * Increments the cycle count and resets layer tracking.
     */
    public void incrementCycle() {
        this.cycleCount++;
        this.hasVisitedAllLayers = false;
        this.visitedLayers.clear();
        this.visitedLayers.add(currentLayer);
    }

    /**
     * Adds a memory to retain between cycles.
     */
    public void addRetainedMemory(String memory) {
        this.retainedMemories.add(memory);
    }

    /**
     * Retains the highest stat from the previous cycle.
     */
    public void retainBestStat() {
        int maxStat = Math.max(Math.max(weird, cool), Math.max(sharp, Math.max(hot, charm)));
        if (weird == maxStat) weird++;
        else if (cool == maxStat) cool++;
        else if (sharp == maxStat) sharp++;
        else if (hot == maxStat) hot++;
        else if (charm == maxStat) charm++;
    }

    /**
     * Checks if the player has visited all layers (win condition).
     */
    public void checkAllLayersVisited() {
        this.hasVisitedAllLayers = visitedLayers.contains(Layer.DREAM) &&
                               visitedLayers.contains(Layer.BASE_REALITY) &&
                               visitedLayers.contains(Layer.DEBUG);
    }

    /**
     * Performs a move (e.g., "Hack the Code") and returns the roll result.
     */
    public String performMove(String moveName, String statName) {
        int statValue = getStatValue(statName);
        return Dice.rollMove(statName, statValue);
    }

    /**
     * Gets the value of a stat by name.
     */
    private int getStatValue(String statName) {
        switch (statName.toLowerCase()) {
            case "weird":
                return weird;
            case "cool":
                return cool;
            case "sharp":
                return sharp;
            case "hot":
                return hot;
            case "charm":
                return charm;
            default:
                return 0;
        }
    }

    /**
     * Returns a summary of the player's stats, playbook, and cycle info.
     */
    public String getStatsSummary() {
        return String.format(
            "👤 %s (%s)\n" +
            "- Cycle: %d\n" +
            "- Weird: %d\n" +
            "- Cool: %d\n" +
            "- Sharp: %d\n" +
            "- Hot: %d\n" +
            "- Charm: %d\n" +
            "- Current Layer: %s",
            name, playbook.getName(), cycleCount, weird, cool, sharp, hot, charm, currentLayer.getName()
        );
    }

    @Override
    public String toString() {
        return getStatsSummary();
    }
}
