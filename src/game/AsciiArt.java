package game;

/**
 * ASCII art for Hidden Gods RPG.
 * Uses only standard ASCII characters for maximum compatibility.
 */
public class AsciiArt {

    // Hidden Gods logo (pure ASCII, no Unicode)
    public static final String LOGO = 
        "   _    _      _    _      _    _   \n" +
        "  | |  | |    | |  | |    | |  | |  \n" +
        "  | |__| | ___| |__| | ___| |__| | __\n" +
        "  |  __  |/ _ \|  __  |/ _ \|  __  |/ /\n" +
        "  | |  | |  __/| |  | |  __/| |  | |  < \n" +
        "  |_|  |_|\___||_|  |_|\___||_|  |_|\_\\_\n" +
        "                                  \n" +
        "   _    _      _    _      _    _   \n" +
        "  | |  | |    | |  | |    | |  | |  \n" +
        "  | |__| | ___| |__| | ___| |__| | __\n" +
        "  |  __  |/ _ \|  __  |/ _ \|  __  |/ /\n" +
        "  | |  | |  __/| |  | |  __/| |  | |  < \n" +
        "  |_|  |_|\___||_|  |_|\___||_|  |_|\_\\_\n";

    // Simplified "HIDDEN GODS" text logo (pure ASCII)
    public static final String LOGO_SIMPLE = 
        "  _   _   _   _   _   _   _   _  \n" +
        " / \ / \ / \ / \ / \ / \ / \ / \ \n" +
        "( H ( I ( D ( D ( E ( N ( G ( O ( D )\n" +
        " \\ /_\\ /_\\ /_\\ /_\\ /_\\ /_\\ /_\\ /_\\ /_\\ /\n" +
        "                                  \n" +
        "  H   H   I   I   D   D   E   N   \n" +
        "  H   H    I    D   D   E   N   G   \n" +
        "  HHHHH    I    D   D   EEE N   O   \n" +
        "  H   H    I    D   D   E   N   D   \n" +
        "  H   H   I   I   DDDD   E   N   S   \n";

    // Even simpler: Just the text "HIDDEN GODS" in a box
    public static final String LOGO_TEXT = 
        "+---------------------+\n" +
        "|    HIDDEN GODS     |\n" +
        "+---------------------+\n" +
        "| A game about nested |\n" +
        "| simulations and the|\n" +
        "| gods who shape them.|\n" +
        "+---------------------+";

    // Layer ASCII art (pure ASCII)
    public static final String DREAM_LAYER = 
        "   .-''''''-.\n" +
        "  /          \\\n" +
        " |   DREAM   |\n" +
        " |  LAYER    |\n" +
        "  \\          /\n" +
        "   '-......-'\n" +
        " .-'''''''''''''-.\n" +
        "/                 \\\n" +
        "|   The walls are   |\n" +
        "|   made of time.   |\n" +
        " \\                 /\n" +
        "  '-.............-'\n";

    public static final String BASE_REALITY_LAYER = 
        "  ___________________\n" +
        " /                   \\\n" +
        "|   BASE REALITY     |\n" +
        "|   The 'normal'     |\n" +
        "|   is a lie.        |\n" +
        " \\___________________/\n" +
        "   |               |\n" +
        "   |   WAKE UP.    |\n" +
        "   |_______________|\n";

    public static final String DEBUG_LAYER = 
        "  +--------------+\n" +
        "  |  DEBUG LAYER |\n" +
        "  |  +--------+  |\n" +
        "  |  | 010101 |  |\n" +
        "  |  | ERROR  |  |\n" +
        "  |  +--------+  |\n" +
        "  | SEGMENTATION |\n" +
        "  | FAULT       |\n" +
        "  +--------------+\n";

    // Anomaly ASCII art (pure ASCII)
    public static final String FLOATING_DOOR = 
        "   ______\n" +
        "  /      \\\n" +
        " |  ===  |\n" +
        " |  ===  |\n" +
        "  \\______/\n" +
        "   |    |\n" +
        "   |____|\n";

    public static final String BACKWARD_CLOCK = 
        "   .-----.\n" +
        "  |  .--. |\n" +
        "  |  |  | |\n" +
        "  |  '--' |\n" +
        "   '-----'\n" +
        "     |  |\n" +
        "     |--|\n";

    public static final String TERMINAL_WINDOW = 
        "  +-------------+\n" +
        "  | ERROR:     |\n" +
        "  | Reality   |\n" +
        "  | not found.|\n" +
        "  |            |\n" +
        "  | [Y] Reboot|\n" +
        "  +-------------+\n";

    // Hidden Gods ASCII art (pure ASCII)
    public static final String THE_DREAMER = 
        "   /\\___/\\\n" +
        "  /  o o  \\\n" +
        " (  =^=  )\n" +
        "  \\  ~  /\n" +
        "   '----'\n" +
        "  THE DREAMER\n";

    public static final String THE_ARCHITECT = 
        "   ______\n" +
        "  /      \\\n" +
        " |  ===  |\n" +
        " |  ===  |\n" +
        "  \\______/\n" +
        "   |  |\n" +
        "   |__|\n" +
        "  THE ARCHITECT\n";

    public static final String THE_DEBUGGER = 
        "   +------+\n" +
        "   | 010  |\n" +
        "   | 101  |\n" +
        "   +------+\n" +
        "    /    \\\n" +
        "   /      \\\n" +
        "  THE DEBUGGER\n";

    // Playbook ASCII art (pure ASCII)
    public static final String HACKER_ICON = 
        "  +-----+\n" +
        "  | === |\n" +
        "  | ( ) |\n" +
        "  +-----+\n";

    public static final String GLITCH_ICON = 
        "  +-----+\n" +
        "  | ~~~ |\n" +
        "  | ~~  |\n" +
        "  +-----+\n";

    public static final String ARCHITECT_ICON = 
        "  +-----+\n" +
        "  | === |\n" +
        "  | === |\n" +
        "  +-----+\n";

    // Dividers and borders
    public static final String DIVIDER = "----------------------------------------";
    public static final String THIN_DIVIDER = "----------";
    public static final String BOLD_DIVIDER = "========================================";

    // Print methods
    public static void printLogo() {
        System.out.println(LOGO_TEXT);
    }

    public static void printLayer(Layer layer) {
        switch (layer) {
            case DREAM:
                System.out.println(DREAM_LAYER);
                break;
            case BASE_REALITY:
                System.out.println(BASE_REALITY_LAYER);
                break;
            case DEBUG:
                System.out.println(DEBUG_LAYER);
                break;
        }
    }

    public static void printHiddenGod(HiddenGod god) {
        switch (god.getName()) {
            case "The Dreamer":
                System.out.println(THE_DREAMER);
                break;
            case "The Architect":
                System.out.println(THE_ARCHITECT);
                break;
            case "The Debugger":
                System.out.println(THE_DEBUGGER);
                break;
        }
    }

    public static void printPlaybookIcon(Playbook playbook) {
        switch (playbook) {
            case HACKER:
                System.out.println(HACKER_ICON);
                break;
            case GLITCH:
                System.out.println(GLITCH_ICON);
                break;
            case ARCHITECT:
                System.out.println(ARCHITECT_ICON);
                break;
            default:
                System.out.println(HACKER_ICON);
        }
    }

    public static void printAnomaly(String anomalyType) {
        switch (anomalyType.toLowerCase()) {
            case "door":
            case "floating door":
                System.out.println(FLOATING_DOOR);
                break;
            case "clock":
            case "backward clock":
                System.out.println(BACKWARD_CLOCK);
                break;
            case "terminal":
            case "terminal window":
                System.out.println(TERMINAL_WINDOW);
                break;
        }
    }

    public static void printDivider() {
        System.out.println(DIVIDER);
    }

    public static void printBoldDivider() {
        System.out.println(BOLD_DIVIDER);
    }

    /**
     * Prints a centered title with borders.
     */
    public static void printTitle(String title) {
        int length = title.length();
        String border = "+" + "-".repeat(Math.max(0, length + 2)) + "+";
        System.out.println(border);
        System.out.println("| " + title + " |");
        System.out.println(border);
    }

    /**
     * Prints a loading animation (for fun).
     */
    public static void printLoading() {
        String[] frames = {"-", "\\", "|", "/"};
        for (String frame : frames) {
            System.out.print("\r" + frame + " Loading...");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        System.out.println("\r+ Ready!          ");
    }
}
