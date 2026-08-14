/**
 * User roles & permissions.
 *
 * Members track their own data; trainers create and assign plans and (if
 * shared) monitor members. Privacy is member-controlled: a member chooses what
 * metrics a trainer can see. The role gates UI affordances across the app.
 */

export type Role = "member" | "trainer";

export type Goal =
  | "resilience"
  | "longevity"
  | "endurance"
  | "strength"
  | "hypertrophy"
  | "mobility"
  | "work_capacity"
  | "cardio";

export type Experience = "beginner" | "intermediate" | "advanced";

export interface UserProfile {
  id: string;
  name: string;
  role: Role;
  // Onboarding quiz results (spec §9).
  goals: Goal[];
  weeklyFrequency: number; // 1-6 gym days/week
  experience: Experience;
  injuries: string[];
  dietChoice?: "Kauffmann" | "Paleo" | "Whole30";
  hrvBaseline?: number; // ms, personal baseline
  // Privacy: which metrics the member shares with their trainer.
  shareWithTrainer: {
    workouts: boolean;
    checkins: boolean;
    journal: boolean;
  };
  onboarded: boolean;
}

export function defaultProfile(name = "You"): UserProfile {
  return {
    id: crypto.randomUUID(),
    name,
    role: "member",
    goals: ["resilience", "longevity"],
    weeklyFrequency: 3,
    experience: "intermediate",
    injuries: [],
    hrvBaseline: 50,
    shareWithTrainer: { workouts: true, checkins: true, journal: false },
    onboarded: false,
  };
}

/** Can the user create/edit workouts and templates? */
export function canEditPlans(role: Role): boolean {
  return role === "trainer";
}

/** Can the user assign plans to members? */
export function canAssign(role: Role): boolean {
  return role === "trainer";
}

/** Filter a member's data down to what they've consented to share. */
export function sharedMetrics<T extends { kind: "workout" | "checkin" | "journal" }>(
  items: T[],
  profile: UserProfile
): T[] {
  if (profile.role === "trainer") return items;
  return items.filter((item) => {
    if (item.kind === "workout") return profile.shareWithTrainer.workouts;
    if (item.kind === "checkin") return profile.shareWithTrainer.checkins;
    return profile.shareWithTrainer.journal;
  });
}
