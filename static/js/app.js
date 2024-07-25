const form = document.getElementById('predictionForm');
const result = document.querySelector('#result');

const handleSubmit = async (e) => {
    e.preventDefault();

    const Pclass = document.getElementById('Pclass').value;
    const Sex = document.getElementById('Sex').value;
    const Age = document.getElementById('Age').value;
    const SibSp = document.getElementById('SibSp').value;
    const Embarked = document.getElementById('Embarked').value;

    const data = {
        Pclass,
        Sex,
        Age,
        SibSp,
        Embarked
    };

    console.log(data);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const resultData = await response.json();

        const p = document.createElement('p');
        if (resultData.prediction === 1) {
            p.className = 'text-red-500 font-bold text-2xl mt-4 text-center bg-red-100 p-4 shadow-md border-l-4 border-red-400';
            p.textContent = `Predicción: ${resultData.prediction} - El paciente tiene un riesgo alto de padecer Cáncer`;
        } else {
            p.className = 'text-green-500 font-bold text-2xl mt-4 text-center bg-green-100 p-4 shadow-md border-l-4 border-green-500';
            p.textContent = `Predicción: ${resultData.prediction} - El paciente tiene un riesgo bajo de padecer Cáncer`;
        }

        result.innerHTML = '';
        result.appendChild(p);

        setTimeout(() => {
            p.remove();
        }, 5000);
    } catch (error) {
        console.error('Error:', error);
    }
};

form.addEventListener('submit', handleSubmit);
