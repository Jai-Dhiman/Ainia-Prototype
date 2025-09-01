"""Learning integration for different educational focuses."""


class LearningIntegrator:
    def embed_math_challenge(self, theme, child_name, difficulty_level="easy"):
        if difficulty_level == "easy":
            if theme == "dragons":
                return f"""
                Create a short adventure story for {child_name} (age 5-9) about dragons.
                Include a counting/simple addition problem naturally in the story.
                Example: "The friendly dragon found 3 golden eggs in one cave and 2 silver eggs in another cave. How many eggs did the dragon find in total?"
                Make it safe, positive, and engaging. End with the math question for {child_name} to solve.
                """
            elif theme == "pirates":
                return f"""
                Create a short adventure story for {child_name} (age 5-9) about pirates.
                Include a counting/simple addition problem naturally in the story.
                Example: "Captain {child_name} discovered 4 gold coins buried under the palm tree and 3 more coins hidden in the treasure chest. How many coins did you find altogether?"
                Make it safe, positive, and engaging. End with the math question for {child_name} to solve.
                """
            elif theme == "princesses":
                return f"""
                Create a short adventure story for {child_name} (age 5-9) about princesses.
                Include a counting/simple addition problem naturally in the story.
                Example: "Princess {child_name} picked 5 beautiful flowers for the castle garden and found 2 more blooming by the fountain. How many flowers does the princess have now?"
                Make it safe, positive, and engaging. End with the math question for {child_name} to solve.
                """
    
    def embed_vocabulary_challenge(self, theme, child_name, age_level="5-9"):
        if theme == "dragons":
            return f"""
            Create a short adventure story for {child_name} (age 5-9) about dragons.
            Include a vocabulary challenge naturally in the story using an age-appropriate word.
            Example: "The dragon showed {child_name} a mysterious word carved in ancient stone: 'COURAGE'. What do you think this word means?"
            Use words like: brave, adventure, treasure, magical, friendship, courage, explore, discover.
            Make it safe, positive, and engaging. End with asking {child_name} to explain what the word means.
            """
        elif theme == "pirates":
            return f"""
            Create a short adventure story for {child_name} (age 5-9) about pirates.
            Include a vocabulary challenge naturally in the story using an age-appropriate word.
            Example: "The treasure map had a special word written on it: 'COMPASS'. Can you tell Captain {child_name} what this word means?"
            Use words like: voyage, compass, treasure, island, adventure, brave, explore, discover.
            Make it safe, positive, and engaging. End with asking {child_name} to explain what the word means.
            """
        elif theme == "princesses":
            return f"""
            Create a short adventure story for {child_name} (age 5-9) about princesses.
            Include a vocabulary challenge naturally in the story using an age-appropriate word.
            Example: "The wise fairy gave Princess {child_name} a scroll with the word 'KINDNESS' written in golden letters. What does this important word mean?"
            Use words like: kindness, wisdom, courage, friendship, magical, graceful, gentle, compassion.
            Make it safe, positive, and engaging. End with asking {child_name} to explain what the word means.
            """
    
    def embed_problem_solving_challenge(self, theme, child_name):
        if theme == "dragons":
            return f"""
            Create a short adventure story for {child_name} (age 5-9) about dragons.
            Include a simple problem-solving challenge naturally in the story.
            Example: "The baby dragon is stuck on the other side of the river, but the bridge is broken. How can {child_name} help the dragon get across safely?"
            Make it safe, positive, and engaging. End with asking {child_name} to think of a creative solution.
            """
        elif theme == "pirates":
            return f"""
            Create a short adventure story for {child_name} (age 5-9) about pirates.
            Include a simple problem-solving challenge naturally in the story.
            Example: "Captain {child_name}'s ship needs to reach the treasure island, but there are rocks blocking the way. How can you safely navigate around them?"
            Make it safe, positive, and engaging. End with asking {child_name} to think of a creative solution.
            """
        elif theme == "princesses":
            return f"""
            Create a short adventure story for {child_name} (age 5-9) about princesses.
            Include a simple problem-solving challenge naturally in the story.
            Example: "Princess {child_name} wants to help the sad unicorn find its way back to the magical forest, but the path is covered with thorny vines. How can the princess help?"
            Make it safe, positive, and engaging. End with asking {child_name} to think of a creative solution.
            """