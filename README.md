**Before running the program, please ensure you have opened it within the correct folder, otherwise, the JSON files that store the words may be created in random locations and could be accidentally deleted!**

# Word Learning Application in Python

This is a Python application designed to help users learn and manage vocabulary through a graphical user interface created with Tkinter. The application supports multiple features, including adding words, testing knowledge, and managing learned and missing words.

## Features

- **Add Words**: Add new English words along with their Turkish translations to the vocabulary list.
- **Test Words**: Test your knowledge of words in the vocabulary list. The application keeps track of the score and moves words to different categories based on performance.
- **Manage Learned Words**: Keep track of words that have been learned. Words can be reviewed and managed through a dedicated section.
- **Manage Missing Words**: Handle words that need further review. Words are moved to this section if answered incorrectly and reintroduced when correctly answered.
- **V1/V2/V3 Words**: Special feature to manage and test words with three levels of vocabulary (V1, V2, V3) and track progress.

## File Structure

- `kelimeler.json`: Stores the main vocabulary with words, their translations, and scores.
- `eksik_kelimeler.json`: Contains words that are missing or need further review.
- `ezberlenen_kelimeler.json`: Keeps track of learned words.
- `kelimeler_v3.json`: Stores V1, V2, and V3 vocabulary with scores.

## Usage

1. **Add Words**: Enter the English and Turkish words in the 'Add Word' tab and click "Add Word" to save.
2. **Test Words**: In the 'Learn Word' tab, test your knowledge of words from the main vocabulary list. The application will track your progress and adjust scores accordingly.
3. **Manage Missing Words**: Use the 'Missing Words' tab to review and test words that need more practice.
4. **Manage Learned Words**: In the 'Learned Words' tab, review and manage words that have been learned.
5. **V1/V2/V3 Words**: Add and test words with multiple levels of vocabulary using the 'V1, V2, V3 Words' and 'V1, V2, V3 Test' tabs.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with any improvements or fixes.


## Contact

For any questions or suggestions, please contact [batuhannakcan@gmail.com](mailto:batuhannakcan@gmail.com).
