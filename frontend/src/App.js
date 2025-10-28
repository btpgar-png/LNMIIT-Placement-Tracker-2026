import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

// Use env-provided API URL when available; default to same-origin '/api'
const API_URL = process.env.REACT_APP_API_URL || "/api";

function App() {
  const [companies, setCompanies] = useState([]);
  const [stats, setStats] = useState({});
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
  const [ctcFilter, setCtcFilter] = useState("all");
  const [showModal, setShowModal] = useState(false);
  const [editingCompany, setEditingCompany] = useState(null);
  const [formData, setFormData] = useState({
    notification_date: "",
    company_name: "",
    type_of_offer: "",
    branches_allowed: "",
    eligibility_cgpa: "",
    job_roles: "",
    ctc_stipend: "",
    students_selected: "",
    process: "Completed",
  });
  const [adminToken, setAdminToken] = useState(
    () => localStorage.getItem("adminToken") || ""
  );
  const [adminValid, setAdminValid] = useState(false);
  const [adminChecking, setAdminChecking] = useState(false);

  useEffect(() => {
    // Invalidate admin when token changes
    setAdminValid(false);
  }, [adminToken]);

  const validateAdmin = async () => {
    if (!adminToken) {
      setAdminValid(false);
      return;
    }
    try {
      setAdminChecking(true);
      await axios.get(`${API_URL}/auth/check`, {
        headers: { "X-Admin-Token": adminToken },
      });
      setAdminValid(true);
    } catch (e) {
      console.error("Admin token invalid", e);
      setAdminValid(false);
      alert("Invalid admin token");
    } finally {
      setAdminChecking(false);
    }
  };

  useEffect(() => {
    fetchCompanies();
    fetchStats();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await axios.get(`${API_URL}/companies`);
      setCompanies(response.data);
    } catch (error) {
      console.error("Error fetching companies:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSort = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") {
      direction = "desc";
    }
    setSortConfig({ key, direction });
  };

  // Extract CTC value for filtering
  const getCtcValue = (ctcText) => {
    if (!ctcText) return 0;
    // Look for "CTC: ₹X" or "Fixed - X"
    const ctcMatch = ctcText.match(/CTC:\s*₹?[\d,]+/i);
    if (ctcMatch) {
      const numbers = ctcText.match(/₹?([\d,]+)/g);
      if (numbers && numbers[0]) {
        return parseFloat(numbers[0].replace(/[₹,]/g, "")) || 0;
      }
    }
    const fixedMatch = ctcText.match(/Fixed\s*-\s*₹?([\d,]+)/i);
    if (fixedMatch) {
      return parseFloat(fixedMatch[1].replace(/,/g, "")) || 0;
    }
    return 0;
  };

  const filteredAndSortedCompanies = companies
    .filter((company) => {
      // Search filter
      const matchesSearch = company.company_name
        .toLowerCase()
        .includes(searchTerm.toLowerCase());

      // CTC filter
      if (ctcFilter === "all") return matchesSearch;

      const ctcValue = getCtcValue(company.ctc_stipend);
      const threshold = parseInt(ctcFilter) * 100000; // Convert lakhs to actual value
      return matchesSearch && ctcValue >= threshold;
    })
    .sort((a, b) => {
      if (!sortConfig.key) return 0;

      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];

      if (typeof aValue === "string") {
        const comparison = aValue.localeCompare(bValue);
        return sortConfig.direction === "asc" ? comparison : -comparison;
      } else if (typeof aValue === "number") {
        return sortConfig.direction === "asc"
          ? aValue - bValue
          : bValue - aValue;
      }

      return 0;
    });

  const handleAddClick = () => {
    setEditingCompany(null);
    setFormData({
      notification_date: "",
      company_name: "",
      type_of_offer: "",
      branches_allowed: "",
      eligibility_cgpa: "",
      job_roles: "",
      ctc_stipend: "",
      students_selected: "",
    });
    setShowModal(true);
  };

  const handleEditClick = (company) => {
    setEditingCompany(company);
    setFormData({
      notification_date: company.notification_date,
      company_name: company.company_name,
      type_of_offer: company.type_of_offer,
      branches_allowed: company.branches_allowed || "",
      eligibility_cgpa: company.eligibility_cgpa || "",
      job_roles: company.job_roles,
      ctc_stipend: company.ctc_stipend,
      students_selected: company.students_selected,
      process: company.process || "Completed",
    });
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        ...formData,
        students_selected: parseInt(formData.students_selected),
      };

      if (editingCompany) {
        await axios.put(`${API_URL}/companies/${editingCompany.id}`, data, {
          headers: { "X-Admin-Token": adminToken },
        });
      } else {
        await axios.post(`${API_URL}/companies`, data, {
          headers: { "X-Admin-Token": adminToken },
        });
      }

      setShowModal(false);
      fetchCompanies();
      fetchStats();
    } catch (error) {
      console.error("Error saving company:", error);
      alert("Admin authorization failed or error saving. Check admin token.");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this record?")) {
      try {
        await axios.delete(`${API_URL}/companies/${id}`, {
          headers: { "X-Admin-Token": adminToken },
        });
        fetchCompanies();
        fetchStats();
      } catch (error) {
        console.error("Error deleting company:", error);
        alert(
          "Admin authorization failed or error deleting. Check admin token."
        );
      }
    }
  };

  const formatCurrency = (value) => {
    if (!value) return value;
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(value);
  };

  const getCurrentDate = () => {
    const today = new Date();
    const day = today.getDate().toString().padStart(2, "0");
    const month = (today.getMonth() + 1).toString().padStart(2, "0");
    const year = today.getFullYear();
    return `${day}/${month}/${year}`;
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>LNMIIT Placement Tracker 2026</h1>
          <div className="last-updated">Last Updated: {getCurrentDate()}</div>
          <div
            style={{
              display: "flex",
              gap: "8px",
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            <input
              type="password"
              placeholder="Admin token"
              value={adminToken}
              onChange={(e) => {
                setAdminToken(e.target.value);
                localStorage.setItem("adminToken", e.target.value);
              }}
              style={{ padding: "6px 8px", minWidth: "220px" }}
            />
            <button
              onClick={validateAdmin}
              disabled={adminChecking}
              className="insights-button"
            >
              {adminChecking ? "Checking..." : "Validate"}
            </button>
            <span
              style={{ fontSize: 12, color: adminValid ? "green" : "#888" }}
            >
              {adminValid ? "Admin mode active" : "Read-only"}
            </span>
            <button
              className="insights-button"
              onClick={() => alert("View Insights feature coming soon!")}
            >
              View Insights
            </button>
          </div>
        </div>

        <div className="stats-container">
          <div className="stat-card">
            <div className="stat-title">Total Unique Companies</div>
            <div className="stat-value">
              {stats.total_unique_companies || 0}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-title">Average Stipend Secured</div>
            <div className="stat-value">
              {formatCurrency(stats.average_stipend || 0)}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-title">Average CTC Offered</div>
            <div className="stat-value">
              {formatCurrency(stats.average_ctc || 0)}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-title">Average Fixed Package Secured</div>
            <div className="stat-value">
              {formatCurrency(stats.average_ctc_weighted || 0)}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-title">Median Package Secured</div>
            <div className="stat-value">
              {formatCurrency(stats.median_ctc || 0)}
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-title">Students Selected</div>
            <div className="stat-value">{stats.students_selected || 0}/490</div>
          </div>
        </div>

        <div className="placement-section">
          <div className="section-title">Placement Data</div>

          <div
            className="search-container"
            style={{ display: "flex", gap: "10px", marginBottom: "20px" }}
          >
            <input
              type="text"
              className="search-input"
              placeholder="Search company..."
              value={searchTerm}
              onChange={handleSearch}
              style={{ flex: 1 }}
            />
            <select
              value={ctcFilter}
              onChange={(e) => setCtcFilter(e.target.value)}
              style={{
                padding: "12px 20px",
                fontSize: "1rem",
                borderRadius: "8px",
                border: "1px solid #ddd",
                backgroundColor: "white",
                cursor: "pointer",
              }}
            >
              <option value="all">All Companies</option>
              <option value="7">Above ₹7 Lakh CTC</option>
              <option value="10">Above ₹10 Lakh CTC</option>
              <option value="12">Above ₹12 Lakh CTC</option>
              <option value="15">Above ₹15 Lakh CTC</option>
              <option value="20">Above ₹20 Lakh CTC</option>
              <option value="25">Above ₹25 Lakh CTC</option>
            </select>
          </div>

          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th onClick={() => handleSort("id")}>
                    # <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("notification_date")}>
                    Notification Date <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("company_name")}>
                    Company Name <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("type_of_offer")}>
                    Type of Offer <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("branches_allowed")}>
                    Branches Allowed <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("eligibility_cgpa")}>
                    Eligibility CGPA <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("job_roles")}>
                    Job Roles <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("ctc_stipend")}>
                    CTC/Stipend <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("students_selected")}>
                    Students Selected <span className="sort-arrows">⇅</span>
                  </th>
                  <th onClick={() => handleSort("process")}>
                    Process <span className="sort-arrows">?</span>
                  </th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredAndSortedCompanies.map((company, index) => (
                  <tr key={company.id}>
                    <td>{index + 1}</td>
                    <td>
                      {new Date(company.notification_date).toLocaleDateString(
                        "en-GB"
                      )}
                    </td>
                    <td>{company.company_name}</td>
                    <td>{company.type_of_offer}</td>
                    <td>{company.branches_allowed || "N/A"}</td>
                    <td>{company.eligibility_cgpa || "N/A"}</td>
                    <td>{company.job_roles}</td>
                    <td>{company.ctc_stipend}</td>
                    <td>{company.students_selected}</td>
                    <td>{company.process || "Completed"}</td>
                    <td>
                      {adminValid && (
                        <>
                          <button
                            onClick={() => handleEditClick(company)}
                            style={{
                              marginRight: "5px",
                              padding: "5px 10px",
                              cursor: "pointer",
                            }}
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDelete(company.id)}
                            style={{
                              padding: "5px 10px",
                              cursor: "pointer",
                              background: "#dc3545",
                              color: "white",
                              border: "none",
                              borderRadius: "4px",
                            }}
                          >
                            Delete
                          </button>
                        </>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {adminValid && (
          <div className="add-button-container">
            <button className="add-button" onClick={handleAddClick}>
              + Add Company
            </button>
          </div>
        )}

        {showModal && (
          <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <div className="modal-title">
                  {editingCompany ? "Edit Company" : "Add New Company"}
                </div>
                <button
                  className="close-button"
                  onClick={() => setShowModal(false)}
                >
                  ×
                </button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label className="form-label">Notification Date</label>
                  <input
                    type="date"
                    className="form-input"
                    value={formData.notification_date}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        notification_date: e.target.value,
                      })
                    }
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Company Name</label>
                  <input
                    type="text"
                    className="form-input"
                    value={formData.company_name}
                    onChange={(e) =>
                      setFormData({ ...formData, company_name: e.target.value })
                    }
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Type of Offer</label>
                  <input
                    type="text"
                    className="form-input"
                    value={formData.type_of_offer}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        type_of_offer: e.target.value,
                      })
                    }
                    placeholder="e.g., PPO, Intern, FTE, Intern+FTE"
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Branches Allowed</label>
                  <input
                    type="text"
                    className="form-input"
                    value={formData.branches_allowed}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        branches_allowed: e.target.value,
                      })
                    }
                    placeholder="e.g., COE, COPC, ECE, ENC, COBS"
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Eligibility CGPA</label>
                  <input
                    type="text"
                    className="form-input"
                    value={formData.eligibility_cgpa}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        eligibility_cgpa: e.target.value,
                      })
                    }
                    placeholder="e.g., 7.5 or N.A."
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Job Roles</label>
                  <input
                    type="text"
                    className="form-input"
                    value={formData.job_roles}
                    onChange={(e) =>
                      setFormData({ ...formData, job_roles: e.target.value })
                    }
                    placeholder="e.g., SDE-I, DS-I, Decision Analytics Associate"
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">CTC/Stipend</label>
                  <textarea
                    className="form-textarea"
                    value={formData.ctc_stipend}
                    onChange={(e) =>
                      setFormData({ ...formData, ctc_stipend: e.target.value })
                    }
                    placeholder="e.g., CTC: ₹14,15,600 or Stipend: ₹27,000/month"
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Students Selected</label>
                  <input
                    type="number"
                    className="form-input"
                    value={formData.students_selected}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        students_selected: e.target.value,
                      })
                    }
                    required
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Process</label>
                  <select
                    className="form-input"
                    value={formData.process}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        process: e.target.value,
                      })
                    }
                  >
                    <option value="Completed">Completed</option>
                    <option value="Pending">Pending</option>
                  </select>
                </div>

                <div className="form-buttons">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setShowModal(false)}
                  >
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {editingCompany ? "Update" : "Add"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
