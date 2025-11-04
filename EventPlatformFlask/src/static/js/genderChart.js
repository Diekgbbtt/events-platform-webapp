document.addEventListener('DOMContentLoaded', function() {
    const maleCount = parseInt(document.getElementById('genderChart').dataset.male);
    const femaleCount = parseInt(document.getElementById('genderChart').dataset.female);
    const unknownCount = parseInt(document.getElementById('genderChart').dataset.unknown);

    const canvas = document.getElementById('genderChart');
    const ctx = canvas.getContext('2d');

    const chartWidth = 500;
    const chartHeight = 200;
    const barWidth = 100;
    const maxCount = Math.max(maleCount, femaleCount, unknownCount);
    const scaleFactor = (chartHeight - 20) / maxCount;  
    
    const maleBarX = 50;  
    const femaleBarX = 200; 
    const unknownBarX = 350; 

    ctx.fillStyle = 'rgba(54, 162, 235, 0.6)';
    ctx.fillRect(maleBarX, chartHeight - maleCount * scaleFactor, barWidth, maleCount * scaleFactor);
    ctx.fillStyle = '#000';
    ctx.fillText('Male', maleBarX + barWidth / 2 - 15, chartHeight - 5); 

    ctx.fillStyle = 'rgba(255, 99, 132, 0.6)';
    ctx.fillRect(femaleBarX, chartHeight - femaleCount * scaleFactor, barWidth, femaleCount * scaleFactor);
    ctx.fillStyle = '#000';
    ctx.fillText('Female', femaleBarX + barWidth / 2 - 20, chartHeight - 5); 

    ctx.fillStyle = 'rgba(153, 102, 255, 0.6)';
    ctx.fillRect(unknownBarX, chartHeight - unknownCount * scaleFactor, barWidth, unknownCount * scaleFactor);
    ctx.fillStyle = '#000';
    ctx.fillText('Unknown', unknownBarX + barWidth / 2 - 25, chartHeight - 5); 

    ctx.fillStyle = '#000';
    ctx.fillText(maleCount, maleBarX + barWidth / 2 - 10, chartHeight - maleCount * scaleFactor - 10);
    ctx.fillText(femaleCount, femaleBarX + barWidth / 2 - 10, chartHeight - femaleCount * scaleFactor - 10);
    ctx.fillText(unknownCount, unknownBarX + barWidth / 2 - 10, chartHeight - unknownCount * scaleFactor - 10);
});
