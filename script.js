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
  
      submitBtn.addEventListener("click", async () => {
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

      collapsedBar.addEventListener("click", () => {
        const isOpen = collapsedBar.classList.toggle("open");
        if (isOpen) {
          formArea.classList.remove("hidden");
        } else {
          formArea.classList.add("hidden");
        }
      });
        try {
        const response = await fetch("ex.json");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const providers = await response.json();
  
        providers.slice(0,10).forEach((pro) => {
          const li = document.createElement("li");
          li.classList.add("provider_item");
          if (pro.name && pro.name !== "unknown" && pro.specialty && pro.specialty !== "unknown" && pro.phone && pro.phone !== "unknown")
          li.innerHTML = `${pro.name} — ${pro.specialty}<br>${pro.phone}`;
          if (pro.name && pro.name !== "unknown" && ( (!pro.specialty || pro.specialty === "unknown") && pro.phone && pro.phone !== "unknown"))
          li.innerHTML = `${pro.name}<br>${pro.phone}`;
          if (pro.name && pro.name !== "unknown" && pro.specialty && pro.specialty !== "unknown" && (!pro.phone || pro.phone === "unknown"))
          li.innerHTML = `${pro.name} — ${pro.specialty}`;
          if (pro.name && pro.name !== "unknown" && ( (!pro.specialty || pro.specialty === "unknown") && (!pro.phone || pro.phone === "unknown")))
          li.innerHTML = `${pro.name}`;
          
          li.addEventListener("click", () => {
            let contactHTML = `<div class="info_section contact_info"><h2 class="pro_namee">${pro.name}</h2>`;
            if (pro.address && pro.address !== "unknown")
              contactHTML += `<p><strong>Address:</strong> ${pro.address}</p>`;
            if (pro.specialty && pro.specialty !== "unknown")
              contactHTML += `<p><strong>Specialty:</strong> ${pro.specialty}</p>`;
            if (pro.phone && pro.phone !== "unknown")
              contactHTML += `<p><strong>Phone:</strong> ${pro.phone}</p>`;
            if (pro.email && pro.email !== "unknown")
              contactHTML += `<p><strong>Email:</strong> ${pro.email}</p>`;
            contactHTML += `</div>`;
            let detailsHTML = `<div class="info_section details_info">`;
            if (pro.website && pro.website !== "unknown")
              detailsHTML += `<p><strong>Website:</strong> <a class="web_link" href="https://${pro.website}" target="_blank">${pro.website}</a></p>`;
            if (pro.accepting_new_clients !== undefined && pro.accepting_new_clients !== "unknown")
              detailsHTML += `<p><strong>Accepting New Clients:</strong> ${pro.accepting_new_clients ? "Yes" : "No"}</p>`;
            if (pro.all_ages) {
              detailsHTML += `<p><strong>All Ages:</strong> Yes</p>`;
            } else if (pro.ages_covered && pro.ages_covered !== "unknown") {
              const ages_covered = pro.ages_covered.replaceAll("[", "").replaceAll("]", "").replaceAll(",", "-").trim();
              detailsHTML += `<p><strong>Ages Covered:</strong> ${ages_covered}</p>`;
            }
            if (pro.schedule && pro.schedule !== "unknown" && pro.schedule.trim() !== "") {
              let scheduleText = pro.schedule.replaceAll("\\n", "\n").replaceAll("<br>", "\n");
              detailsHTML += `<p><strong>Schedule:</strong></p><pre class="schedule">${scheduleText.trim()}</pre>`;
            }
            if (Array.isArray(pro.tags)) {
              const validTags = pro.tags.filter(t => t && t !== "unknown").slice(0, 6);
              if (validTags.length) {
                const tagHTML = validTags.map(t => `<span class="tag">${t}</span>`).join(" ");
                detailsHTML += `<p><strong>Associated tags:</strong><br>${tagHTML}</p>`;
              }
            }
            detailsHTML += `</div>`;
            providerInfo.innerHTML = contactHTML + detailsHTML;
          });
          providerList.appendChild(li);
        });
      } catch (error) {
        console.error("Error loading or parsing JSON:", error);
        return null;
      }
    });
  });
  