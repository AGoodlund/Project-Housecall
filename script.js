document.addEventListener("DOMContentLoaded", () => {
    const formArea = document.getElementById("form_area");
    const collapsedBar = document.getElementById("collapsed_bar");
    const collapsedLabel = document.getElementById("collapsed_label");
    const providerSection = document.getElementById("provider_section");
    const submitBtn = document.getElementById("submit_btn");
    const validationMsg = document.getElementById("validation_message");
    const zipInput = document.getElementById("zip_code");
    const textInput = document.getElementById("text_input");
    const providerList = document.getElementById("provider_list");
    const providerInfo = document.getElementById("provider_info");
  
    const demoProviders = [
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
      {name: "Test Name",specialty: "random info",phone: "phone number" },
    ];
      submitBtn.addEventListener("click", () => {
        if (!(zipInput.value && textInput.value)) {
            validationMsg.classList.remove("hidden");
            return;
          }
          
      validationMsg.classList.add("hidden");
  
      formArea.classList.add("hidden");
      collapsedBar.style.display = "flex";
      collapsedBar.classList.remove("open");
      collapsedLabel.textContent = `Modify Search:`;
  
      providerSection.classList.remove("hidden");
      providerList.innerHTML = "";
  
      demoProviders.forEach((p) => {
        const li = document.createElement("li");
        li.classList.add("provider_item");
        li.textContent = `${p.name} — ${p.specialty}`;
        li.addEventListener("click", () => {
          providerInfo.innerHTML = `
            <h3>${p.name}</h3>
            <p><strong>Specialty:</strong> ${p.specialty}</p>
            <p><strong>Phone:</strong> ${p.phone}</p>
          `;
        });
        providerList.appendChild(li);
      });
    });
  
    collapsedBar.addEventListener("click", () => {
      const isOpen = collapsedBar.classList.toggle("open");
      if (isOpen) {
        formArea.classList.remove("hidden");
      } else {
        formArea.classList.add("hidden");
      }
    });
  });
  