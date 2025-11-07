// Elements
const studentInput = document.getElementById('studentInput');
const addStudentBtn = document.getElementById('addStudentBtn');
const studentsUl = document.getElementById('students');
const groupSizeInput = document.getElementById('groupSize');
const generateBtn = document.getElementById('generateBtn');
const groupsUl = document.getElementById('groups');

// Load students from localStorage
let students = JSON.parse(localStorage.getItem('students')) || [];
renderStudents();

// Add student
addStudentBtn.addEventListener('click', () => {
  const name = studentInput.value.trim();
  if(name && !students.includes(name)) {
    students.push(name);
    localStorage.setItem('students', JSON.stringify(students));
    renderStudents();
    studentInput.value = '';
  } else {
    alert('Enter a unique student name');
  }
});

// Render students
function renderStudents() {
  studentsUl.innerHTML = '';
  students.forEach((student, index) => {
    const li = document.createElement('li');
    li.textContent = student;
    const removeBtn = document.createElement('button');
    removeBtn.textContent = '❌';
    removeBtn.onclick = () => removeStudent(index);
    li.appendChild(removeBtn);
    studentsUl.appendChild(li);
  });
}

// Remove student
function removeStudent(index) {
  students.splice(index, 1);
  localStorage.setItem('students', JSON.stringify(students));
  renderStudents();
}

// Generate groups
generateBtn.addEventListener('click', () => {
  const groupSize = parseInt(groupSizeInput.value);
  if(!groupSize || groupSize <= 0) {
    alert('Enter a valid group size');
    return;
  }

  const shuffled = [...students].sort(() => 0.5 - Math.random());
  const groups = [];
  for(let i = 0; i < shuffled.length; i += groupSize) {
    groups.push(shuffled.slice(i, i + groupSize));
  }

  renderGroups(groups);
});

// Render groups with colors
function renderGroups(groups) {
  groupsUl.innerHTML = '';
  groups.forEach((group, index) => {
    const li = document.createElement('li');
    li.textContent = `Group ${index + 1}: ${group.join(', ')}`;
    li.classList.add('group-item', `group-${index % 9}`);
    groupsUl.appendChild(li);
  });
}


// Wheel
