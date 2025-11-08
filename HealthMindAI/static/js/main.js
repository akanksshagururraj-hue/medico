function showTab(role) {
    const patientForm = document.getElementById('patientForm');
    const doctorForm = document.getElementById('doctorForm');
    const tabs = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(tab => tab.classList.remove('active'));
    
    if (role === 'patient') {
        patientForm.classList.remove('hidden');
        doctorForm.classList.add('hidden');
        tabs[0].classList.add('active');
    } else {
        patientForm.classList.add('hidden');
        doctorForm.classList.remove('hidden');
        tabs[1].classList.add('active');
    }
}

function viewDetails(id, name, age, gender, symptoms, history, medications, 
                     analysis, priority, summary, fileName, filePath) {
    document.getElementById('modalPatientName').textContent = name;
    document.getElementById('modalAge').textContent = age;
    document.getElementById('modalGender').textContent = gender;
    document.getElementById('modalSymptoms').textContent = symptoms || 'Not provided';
    document.getElementById('modalHistory').textContent = history || 'Not provided';
    document.getElementById('modalMedications').textContent = medications || 'Not provided';
    document.getElementById('modalAnalysis').textContent = analysis || 'Pending analysis';
    document.getElementById('modalSummary').textContent = summary || 'Pending summary';
    document.getElementById('modalDataId').value = id;
    
    const priorityBadge = document.getElementById('modalPriority');
    priorityBadge.textContent = priority;
    priorityBadge.className = 'badge badge-' + priority.toLowerCase();
    
    const fileSection = document.getElementById('fileSection');
    if (fileName) {
        document.getElementById('modalFileName').textContent = fileName;
        fileSection.style.display = 'block';
    } else {
        fileSection.style.display = 'none';
    }
    
    document.getElementById('detailsModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('detailsModal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('detailsModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('patientDataForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const age = document.getElementById('age').value;
            const symptoms = document.getElementById('symptoms').value;
            
            if (age < 1 || age > 120) {
                e.preventDefault();
                alert('Please enter a valid age between 1 and 120');
                return false;
            }
            
            if (symptoms.trim().length < 10) {
                e.preventDefault();
                alert('Please provide more detailed symptoms (at least 10 characters)');
                return false;
            }
        });
    }
});
