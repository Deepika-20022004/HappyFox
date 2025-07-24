// src/components/CompanyList.js
import React, { useState, useEffect } from 'react';
import './css/CompanyList.css'; // For simple CSS

function CompanyList() {
    const [companies, setCompanies] = useState([]);
    const [filteredRole, setFilteredRole] = useState('');
    const [filteredDomain, setFilteredDomain] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchCompanies = async () => {
        setLoading(true);
        setError(null);
        let url = 'http://localhost:8000/api/companies/';
        const params = new URLSearchParams();
        if (filteredRole) {
            params.append('role', filteredRole);
        }
        if (filteredDomain) {
            params.append('domain', filteredDomain);
        }
        if (params.toString()) {
            url += `?${params.toString()}`;
        }

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setCompanies(data);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCompanies();
    }, [filteredRole, filteredDomain]); // Re-fetch when filters change

    const uniqueRoles = [...new Set(companies.map(c => c.role))];
    const uniqueDomains = [...new Set(companies.map(c => c.domain))];


    if (loading) return <div className="loading">Loading companies...</div>;
    if (error) return <div className="error">Error: {error}</div>;

    return (
        <div className="company-list-container">
            <h1>Company Drives</h1>
            <div className="filters">
                <label>Filter by Role: </label>
                <select value={filteredRole} onChange={(e) => setFilteredRole(e.target.value)}>
                    <option value="">All Roles</option>
                    {uniqueRoles.map(role => (
                        <option key={role} value={role}>{role}</option>
                    ))}
                </select>

                <label>Filter by Domain: </label>
                <select value={filteredDomain} onChange={(e) => setFilteredDomain(e.target.value)}>
                    <option value="">All Domains</option>
                    {uniqueDomains.map(domain => (
                        <option key={domain} value={domain}>{domain}</option>
                    ))}
                </select>
            </div>

            <div className="company-cards">
                {companies.length === 0 ? (
                    <p>No companies found matching your criteria.</p>
                ) : (
                    companies.map(company => (
                        <div key={company.id} className="company-card">
                            <h2>{company.company_name}</h2>
                            <p><strong>Role:</strong> {company.role}</p>
                            <p><strong>Domain:</strong> {company.domain}</p>
                            <p><strong>Salary:</strong> {company.salary_range || 'N/A'}</p>
                            <p><strong>Hiring Timeline:</strong> {company.hiring_timeline}</p>
                            <p><strong>Drive Date:</strong> {company.drive_date}</p>
                            <p><strong>Location:</strong> {company.location || 'N/A'}</p>
                            <p><strong>Interview Process:</strong> {company.interview_process_description || 'N/A'}</p>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default CompanyList;