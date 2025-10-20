import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAllUsers, approveUser } from '../../features/admin/adminSlice';
import Swal from 'sweetalert2';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const dispatch = useDispatch();
  const { users, isLoading } = useSelector((state) => state.admin) || { users: [] };

  useEffect(() => {
    dispatch(fetchAllUsers());
  }, [dispatch]);

  const handleApprove = (userId, username) => {
    Swal.fire({
      title: 'Approve Farmer?',
      text: `Are you sure you want to approve ${username}?`,
      icon: 'question',
      showCancelButton: true,
      confirmButtonColor: '#4a7c59',
      confirmButtonText: 'Yes, approve!',
    }).then((result) => {
      if (result.isConfirmed) {
        dispatch(approveUser(userId)).then(action => {
          if (approveUser.fulfilled.match(action)) {
            Swal.fire('Approved!', `${username} has been approved.`, 'success');
          }
        });
      }
    });
  };

  if (isLoading) {
    return <p>Loading users...</p>;
  }

  return (
    <div className="admin-dashboard-container">
      <h2>User Management</h2>
      <table className="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>
                {user.is_approved ? (
                  <span className="status-approved">Approved</span>
                ) : (
                  <span className="status-pending">Pending</span>
                )}
              </td>
              <td>
                {user.role === 'farmer' && !user.is_approved && (
                  <button onClick={() => handleApprove(user.id, user.username)} className="approve-btn">
                    Approve
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;