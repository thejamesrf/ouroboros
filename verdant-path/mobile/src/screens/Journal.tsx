/** Journal screen: free-form notes, tags, photo upload, voice-to-text. */
import React, { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput, View, Pressable } from "react-native";
import { Body, Button, Card, SectionTitle } from "../components/ui";
import { useTheme } from "../theme";
import { spacing } from "../theme/tokens";
import { useAppStore } from "../state/store";
import { makeJournalEntry } from "../domain/tracker";

export default function Journal() {
  const { theme } = useTheme();
  const journal = useAppStore((s) => s.journal);
  const addJournal = useAppStore((s) => s.addJournal);

  const [text, setText] = useState("");
  const [tags, setTags] = useState("");

  const save = () => {
    if (!text.trim()) return;
    addJournal(
      makeJournalEntry({
        id: `je-${Date.now()}`,
        day: new Date(),
        text: text.trim(),
        tags: tags.split(",").map((t) => t.trim()).filter(Boolean),
      })
    );
    setText("");
    setTags("");
  };

  return (
    <ScrollView contentContainerStyle={[styles.container, { backgroundColor: theme.bg }]}>
      <Text style={[styles.title, { color: theme.text }]}>Journal 🪞</Text>

      <Card>
        <SectionTitle>New entry</SectionTitle>
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border }]}
          placeholder="Pain, energy, mood, insights…"
          placeholderTextColor={theme.muted}
          value={text}
          onChangeText={setText}
          multiline
        />
        <TextInput
          style={[styles.input, { color: theme.text, borderColor: theme.border, marginTop: spacing.sm }]}
          placeholder="tags: recovery, soreness, motivation"
          placeholderTextColor={theme.muted}
          value={tags}
          onChangeText={setTags}
        />
        <View style={{ flexDirection: "row", gap: spacing.sm, marginTop: spacing.md }}>
          <Button label="Save entry" onPress={save} />
          <Button label="🎤 Voice" onPress={() => {}} variant="ghost" />
          <Button label="📷 Photo" onPress={() => {}} variant="ghost" />
        </View>
      </Card>

      <SectionTitle>Recent entries</SectionTitle>
      {journal.length === 0 && <Body muted>No entries yet.</Body>}
      {journal.map((e) => (
        <Card key={e.id}>
          <Text style={{ color: theme.muted, fontSize: 12 }}>
            {e.day.toDateString()}
          </Text>
          <Body>{e.text}</Body>
          {e.tags.length > 0 && (
            <View style={{ flexDirection: "row", flexWrap: "wrap", gap: spacing.xs, marginTop: spacing.sm }}>
              {e.tags.map((t) => (
                <View key={t} style={[styles.tag, { borderColor: theme.border }]}>
                  <Text style={{ color: theme.muted }}>#{t}</Text>
                </View>
              ))}
            </View>
          )}
        </Card>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: spacing.lg, paddingBottom: spacing.xxl },
  title: { fontSize: 26, fontWeight: "800", marginBottom: spacing.md },
  input: {
    borderWidth: 1,
    borderRadius: 12,
    padding: spacing.md,
    minHeight: 80,
    textAlignVertical: "top",
  },
  tag: {
    borderWidth: 1,
    borderRadius: 999,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
  },
});
