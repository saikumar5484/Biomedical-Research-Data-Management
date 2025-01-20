const express = require('express');
const fs = require('fs');
const path = require('path');
const XLSX = require('xlsx');

const app = express();
const filePath = '/home/prasad/Downloads/hospital_data.xlsx';

app.use(express.json()); // To parse JSON body

// Endpoint to handle Excel file creation
app.post('/exportData', (req, res) => {
    const data = req.body.data;

    try {
        // Check if the file exists and delete it
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
            console.log('Existing file deleted');
        }

        // Create a new workbook and sheet
        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, "Hospital Data");

        // Write the new file
        XLSX.writeFile(wb, filePath);

        res.status(200).json({ message: 'File created successfully', filePath });
    } catch (error) {
        console.error('Error processing file:', error);
        res.status(500).json({ message: 'Error processing file', error });
    }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
