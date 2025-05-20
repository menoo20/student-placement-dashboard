import React, { useState } from 'react';

const StudentTable = ({ students }) => {
    const [showEditModal, setShowEditModal] = useState(false);
    const [selectedStudent, setSelectedStudent] = useState(null);

    const handleEditClick = (student) => {
        const password = prompt("Please enter the password to edit student information:");
        if (password && password.trim() !== "") {
            setSelectedStudent(student);
            setShowEditModal(true);
        } else {
            setShowEditModal(false);
        }
    };

    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {students.map((student) => (
                    <tr key={student.id}>
                        <td>{student.name}</td>
                        <td>{student.age}</td>
                        <td>
                            <button onClick={() => handleEditClick(student)}>Edit</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default StudentTable;