fetch("/api/trends").then(res => {
    res.json().then(mydataset => {
        console.log(mydataset);
        RenderingCharts(mydataset);
    })
})


function getMonthFromStr(mydatestr = "01/10/2024") {
    // 01/10/2024
    return mydatestr.split("/")[1] + "/" + mydatestr.split("/")[2]
}


function RenderingCharts(dataset) {

    //extract the claims from the dataset
    function getClaimTrends(data) {
        let years = [];
        let amounts = [];
        data.claims.forEach((v) => {
          let current_year = getMonthFromStr(v.date_filed);
          if (!years.includes(current_year)) {
            years.push(current_year);
          }
        });

        amounts = years.map((v) => {
          return getTotal(v);
        });

        function GetYear(myyrstr) {
          return new Date(myyrstr).getFullYear();
        }

        function getTotal(year) {
          let mycurtotal = 0;
          let claimextract = data.claims.filter((v) => {
            return getMonthFromStr(v.date_filed) == year;
          });
          claimextract.forEach((v) => {
            mycurtotal += v.amount;
          });
          return mycurtotal;
        }
        return [years, amounts];
    }



    //extract the number of males and females from the dataset
    function getGenderTrends(data) {
        let malemembersLength = data.members.filter((member) => {
          return member.gender == "male";
        }).length;

        let femalemembersLength = data.members.filter((member) => {
          return member.gender == "female";
        }).length;

        return [
          ["male", "female"],
          [malemembersLength, femalemembersLength],
        ];
    }


    //extract the contributions from the dataset
    function getContributionTrends(data) {
        let periods = [];
        let amounts = [];
        data.contributions.forEach((v) => {
          let current_year = getMonthFromStr(v.period);
          if (!periods.includes(current_year)) {
            periods.push(current_year);
          }
        });
        amounts = periods.map((v) => {
          return getContributionSum(v);
        });


        function getContributionSum(year) {
          let mycurtotal = 0;
          let contributionextract = data.contributions.filter((v) => {
            return getMonthFromStr(v.period) == year;
          });
          contributionextract.forEach((v) => {
            mycurtotal += parseFloat(v.amount);
          });
          return mycurtotal;
        }
        return [periods, amounts];
    }


    //extract the contributionVSclaims from the dataset
    function contributionsVSclaimsTrends(data){
        let dates = [];
        let contribution = [];
        let claim = [];
        data.contributionsVSclaims.forEach((i) =>{
          dates.push(i.period)
          contribution.push(parseFloat(i.contributions))
          claim.push(parseFloat(i.claims))
        });
        console.log(dates, contribution, claim)
        return [dates,contribution,claim]
    }
      
    //creating the claimTrends graph
    function createClaimTrends() {
        const claimFrequencyCtx = document
        .getElementById("claimFrequencyChart")
        .getContext("2d");
      new Chart(claimFrequencyCtx, {
        type: "bar",
        data: {
          labels: getClaimTrends(dataset)[0],
          datasets: [
            {
              label: "Number of Claims",
              data: getClaimTrends(dataset)[1],
              backgroundColor: "rgba(54, 162, 235, 0.6)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: "Number of Claims" },
            },
            x: { title: { display: true, text: "Date Filed" } },
          },
        },
      });

    }
    createClaimTrends()
      //creating the GenderTrends graph
    function createGenderTrends(){
        // Get the data from the function
            const [labels, data] = getGenderTrends(dataset);

            // Chart.js configuration
            const ctx = document.getElementById("genderDonutChart").getContext("2d");
            const genderDonutChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                label: "Gender Distribution",
                data: data,
                backgroundColor: ["#36A2EB", "#FF6384"], // Blue for males, pink for females
                hoverBackgroundColor: ["#5AD3E6", "#FF9AA2"]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.label + ': ' + tooltipItem.raw;
                    }
                    }
                }
                }
            }
    })};
    createGenderTrends()
      //creating the contribution graph
    function createContributionsTrend(){
      // Get the data from the function
      const [labels, data] = getContributionTrends(dataset);
      // Chart.js configuration
      const ctx = document.getElementById("contributionBarChart").getContext("2d");
      const contributionBarChart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [{
              label: "Total Contributions per Year",
              data: data,
              backgroundColor: "rgba(54, 162, 235, 0.6)", // Bar color
              borderColor: "rgba(54, 162, 235, 1)", // Bar border color
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'Total Contributions'
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Month/Year'
                }
              }
            },
            plugins: {
              legend: {
                display: true,
                position: 'top'
              }
            }
          }
      })
    };
      createContributionsTrend()

      //creating the contribution vs claim graph
    function createContributionVSClaim(){
        const [labels, contributionsData, claimsData] = contributionsVSclaimsTrends(dataset);
        // Chart.js configuration
        const ctx = document.getElementById("contributionsVsClaimsChart").getContext("2d");
        const contributionsVsClaimsChart = new Chart(ctx, {
          type: "line",
          data: {
            labels: labels, // Periods
            datasets: [
              {
                label: "Contributions",
                data: contributionsData,
                borderColor: "rgba(54, 162, 235, 1)",
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                tension: 0.4, // Smooth line
              },
              {
                label: "Claims",
                data: claimsData,
                borderColor: "rgba(255, 99, 132, 1)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                tension: 0.4, // Smooth line
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: "top",
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "Period",
                },
              },
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: "Amount(USD)",
                },
              },
            },
          },
        })
    };
    createContributionVSClaim()



}