def ssfp(self, t1_array, TR, FA):
    row, col = self.arr.shape
    theta = np.radians(FA)
    kspace_ssfp = np.zeros((row, col), dtype=np.complex)
    phantom = self.Phantom(row, col)
    # startup cycle with 0.5 theta
    phantom = self.startup_cycle(theta / 2, self.stcy, phantom)
    # rotate and decay
    phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
    # startup cycle with theta
    phantom = self.startup_cycle(theta, self.stcy, phantom)
    for r in range(row):  # rows
        phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
        for c in range(col):
            Gx_step = ((2 * math.pi) / row) * r  # Frequency encodind
            Gy_step = ((2 * math.pi) / col) * c  # Phase encodind
            for i in range(row):
                for j in range(col):
                    Toltal_theta = (Gx_step * i) + (Gy_step * j)
                    Mag = math.sqrt(((phantom[i, j, 0]) * (phantom[i, j, 0])) +
                                    ((phantom[i, j, 1]) * (phantom[i, j, 1])))

                    kspace_ssfp[r, c] = kspace_ssfp[r, c] + (Mag * np.exp(-1j * Toltal_theta))
                    QApplication.processEvents()

            QApplication.processEvents()
        theta = -theta  # for ernst angle
        # print(theta)
        for l in range(row):
            for m in range(col):
                phantom[l, m, 2] = ((phantom[l, m, 2]) * np.exp(-TR / t1_array[l, m])) + (1 - np.exp(
                    -TR / t1_array[l, m]))

        QApplication.processEvents()
    return kspace_ssfp

def rotate(self, theta, phantom):
    RF = ([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    phantom = np.dot(RF, phantom)
    return phantom


def decay(self, phantom, TE, T2):
    dec = np.exp(-TE / T2)
    phantom = np.dot(dec, phantom)
    return phantom


def rotate_decay(self, theta, TE, T2, phantom):
    row, col = self.arr.shape
    for i in range(row):
        for j in range(col):
            phantom[i, j, :] = self.rotate(theta, phantom[i, j, :])
            phantom[i, j, :] = self.decay(phantom[i, j, :], TE, T2[i, j])
    return phantom


def recovery(self, TR, T1, phantom):
    row, col = self.arr.shape
    for i in range(row):
        for j in range(col):
            phantom[i, j, 0] = 0
            phantom[i, j, 1] = 0
            phantom[i, j, 2] = ((phantom[i, j, 2]) * np.exp(
                -TR / T1[i, j])) + (1 - np.exp(-TR / T1[i, j]))
    return phantom


def startup_cycle(self, theta, n, phantom):
    for r in range(n):
        phantom = self.rotate_decay(theta, self.te, self.t2_array, phantom)
        phantom = self.recovery(self.tr, self.t11_array, phantom)
    return phantom


def Phantom(self, row, col):
    phantom = np.zeros((row, col, 3))
    for i in range(row):
        for j in range(col):
            phantom[i, j, 2] = 1
    return phantom
