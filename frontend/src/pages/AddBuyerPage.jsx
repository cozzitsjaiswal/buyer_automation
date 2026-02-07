import { useState } from 'react';
import { api, BUYER_TYPES, PRODUCT_OPTIONS, SOURCE_OPTIONS, STATUS_OPTIONS } from '../api';

const initialForm = {
  company_name: '',
  country: '',
  city: '',
  buyer_type: 'Importer',
  contact_person: '',
  designation: '',
  email: '',
  phone: '',
  website: '',
  source: 'Manual',
  product_interest: 'Turmeric',
  moq: '',
  price_discussed: '',
  payment_terms: '',
  status: 'New',
  last_contact_date: '',
  next_follow_up_date: '',
  remarks: '',
};

export default function AddBuyerPage() {
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState('');

  const onChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const validate = () => {
    if (!form.company_name || !form.country) return 'Company name and country are required.';
    if (form.email && !/^\S+@\S+\.\S+$/.test(form.email)) return 'Invalid email format.';
    return '';
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const error = validate();
    if (error) {
      setMessage(error);
      return;
    }

    try {
      const payload = {
        ...form,
        price_discussed: form.price_discussed ? Number(form.price_discussed) : null,
        last_contact_date: form.last_contact_date || null,
        next_follow_up_date: form.next_follow_up_date || null,
        email: form.email || null,
      };

      await api.post('/buyers', payload);
      setForm(initialForm);
      setMessage('Buyer added successfully.');
    } catch (err) {
      setMessage(err?.response?.data?.detail || 'Failed to save buyer.');
    }
  };

  const field = 'border rounded-md px-3 py-2 bg-white';

  return (
    <div>
      <h2 className="text-2xl font-semibold text-slate-800 mb-5">Add Buyer</h2>
      <form onSubmit={onSubmit} className="bg-white rounded-lg shadow p-5 grid grid-cols-1 md:grid-cols-2 gap-4">
        <input className={field} name="company_name" placeholder="Company Name *" value={form.company_name} onChange={onChange} />
        <input className={field} name="country" placeholder="Country *" value={form.country} onChange={onChange} />
        <input className={field} name="city" placeholder="City" value={form.city} onChange={onChange} />
        <select className={field} name="buyer_type" value={form.buyer_type} onChange={onChange}>{BUYER_TYPES.map((v) => <option key={v}>{v}</option>)}</select>
        <input className={field} name="contact_person" placeholder="Contact Person" value={form.contact_person} onChange={onChange} />
        <input className={field} name="designation" placeholder="Designation" value={form.designation} onChange={onChange} />
        <input className={field} name="email" placeholder="Email" value={form.email} onChange={onChange} />
        <input className={field} name="phone" placeholder="Phone" value={form.phone} onChange={onChange} />
        <input className={field} name="website" placeholder="Website" value={form.website} onChange={onChange} />
        <select className={field} name="source" value={form.source} onChange={onChange}>{SOURCE_OPTIONS.map((v) => <option key={v}>{v}</option>)}</select>
        <select className={field} name="product_interest" value={form.product_interest} onChange={onChange}>{PRODUCT_OPTIONS.map((v) => <option key={v}>{v}</option>)}</select>
        <input className={field} name="moq" placeholder="MOQ" value={form.moq} onChange={onChange} />
        <input className={field} name="price_discussed" type="number" step="0.01" placeholder="Price Discussed" value={form.price_discussed} onChange={onChange} />
        <input className={field} name="payment_terms" placeholder="Payment Terms" value={form.payment_terms} onChange={onChange} />
        <select className={field} name="status" value={form.status} onChange={onChange}>{STATUS_OPTIONS.map((v) => <option key={v}>{v}</option>)}</select>
        <input className={field} type="date" name="last_contact_date" value={form.last_contact_date} onChange={onChange} />
        <input className={field} type="date" name="next_follow_up_date" value={form.next_follow_up_date} onChange={onChange} />
        <textarea className={`${field} md:col-span-2`} name="remarks" placeholder="Remarks" value={form.remarks} onChange={onChange} />

        <div className="md:col-span-2 flex items-center gap-3">
          <button className="bg-emerald-600 text-white px-4 py-2 rounded-md">Save Buyer</button>
          <span className="text-sm text-slate-600">{message}</span>
        </div>
      </form>
    </div>
  );
}
