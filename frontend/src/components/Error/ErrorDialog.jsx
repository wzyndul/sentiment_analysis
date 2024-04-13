import {Button,  Dialog,  DialogActions,  DialogContent,  DialogContentText,  DialogTitle,} from "@mui/material";

const ErrorDialog = ({ open, handleClose, error }) => (
  <Dialog
    open={open}
    onClose={handleClose}
    aria-labelledby="alert-dialog-title"
    aria-describedby="alert-dialog-description"
  >
    <DialogTitle id="alert-dialog-title">{"Error"}</DialogTitle>
    <DialogContent>
      <DialogContentText id="alert-dialog-description">
        {error}
      </DialogContentText>
    </DialogContent>
    <DialogActions>
      <Button onClick={handleClose} color="primary" autoFocus>
        Close
      </Button>
    </DialogActions>
  </Dialog>
);

export default ErrorDialog;
