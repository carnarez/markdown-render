// example with Chart.js (https://www.chartjs.org/)

// load the required external javascript library; could be done globally to avoid
// reloading the same library multiple times with document.head.appendChild(script)
const script = document.createElement("script");
document.getElementById("chart").appendChild(script);

// link to the library cdn
script.src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js";

// once the script is fetched and imported
script.onload = () => {

  // Chart.js works with canvas
  const canvas = document.createElement("canvas");
  document.getElementById("chart").append(canvas);

  // harmonize the chart with the page style
  const style = getComputedStyle(document.body);

  Chart.defaults.borderColor = style.getPropertyValue("--background-color-alt")
  Chart.defaults.color = style.getPropertyValue("--font-color");
  Chart.defaults.font.family = style.fontFamily;
  Chart.defaults.font.size = 0.9 * style.fontSize.match(/[0-9]+/)[0];

  // build the chart
  const data = {
    labels: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
    ],
    datasets: [
      {
        data: [0, 10, 5, 2, 20, 30],
        label: "First dataset",
        backgroundColor: "#ff7b72",
        borderColor: "#ff7b72",
      },
      {
        data: [5, 6, 9, 5, 31, 26],
        label: "Second dataset",
        backgroundColor: "#ffa657",
        borderColor: "#ffa657",
      }
    ]
  };

  const options = {
    scales: {
      x: {
        grid: {
          borderDash: [4, 3]
        }
      },
      y: {
        grid: {
          borderDash: [4, 3]
        }
      }
    }
  }

  const chart = new Chart(
    canvas,
    {
      type: "line",
      data: data,
      options: options
    }
  );

};
