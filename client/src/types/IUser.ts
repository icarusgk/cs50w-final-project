type User = {
  id: number;
  username: string;
  email: string;
  streak: number;
  auto_start_pomos: boolean;
  auto_start_breaks: boolean;
  current_task_id: number | null;
};

export default User;