import spacy


class SimilarityFinder:
    input_text = ""
    def __init__(self, input_text: str):
        self.input_text = input_text
        self.nlp = spacy.load("en_core_web_lg")

    def calculate_similarity(self, sentence1: str, sentence2: str) -> float:
        doc1 = self.nlp(sentence1)
        doc2 = self.nlp(sentence2)
        similarity_score = doc1.similarity(doc2)
        return similarity_score

    def findSimilarity(self):
        result_text = open('ml/result.txt', 'r', encoding='utf-8')
        final_output = open('ml/final_output.txt', 'w+', encoding='utf-8')
        count = 0
        similarity_score_list = []
        temporary_sentence = ""
        for line in result_text:

            final_output.write(line)

            if line.count('Link'):
                final_output.write("\n")

            if line.count('Title'):# Title and snippet is concatenated for better comparison
                temporary_sentence = line

            elif line.count('Snippet'):
                count += 1
                found = temporary_sentence + line
                temporary_sentence = ""
                similarity_score = self.calculate_similarity(self.input_text, found)
                similarity_score_list.append(similarity_score)

                # Storing the similarity score
                # final_output.write("-------------------------------------------------------------------\n")
                # final_output.write(self.input_text)
                # final_output.write(found)
                final_output.write(f"\n[Case {count}]: Context Similarity between the two sentences: {similarity_score * 100: .2f}%\n")
                # final_output.write("-------------------------------------------------------------------\n\n")


        # Additional Data
        final_output.write(f"\nAverage Context Similarity between the two sentences: {sum(similarity_score_list) / len(similarity_score_list) * 100: .2f}%")
        final_output.write(f"\nMax Context Similarity between the two sentences: {max(similarity_score_list) * 100: .2f}%")
        final_output.close()